"""
LinkedIn Job Assistant MCP Server
===================================
Tools:
  - scrape_job          → Scrape a LinkedIn job posting
  - tailor_resume       → AI subagent tailors resume to the job
  - draft_cover_letter  → AI subagent writes a cover letter
  - log_application     → Log the application to a tracker file
  - view_applications   → View all tracked applications
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import anthropic
from mcp.server.fastmcp import FastMCP

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ai = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
mcp = FastMCP("linkedin-assistant")

# ── Your resume (baked in) ────────────────────────────────────────────────────
RESUME = """
Ajay Rao
480-265-5579 | ajayrao0116@gmail.com

SUMMARY
Highly driven Computer Science undergraduate with hands-on educational experience building 
intelligent applications using large language models, NLP pipelines, and data-driven systems. 
Passionate about developing scalable AI solutions and eager to apply machine learning and 
software engineering skills to solve real-world problems.

EDUCATION
San Diego State University, CA | GPA: 3.53
Bachelor of Science in Computer Science — Junior (Expected May 2027)

COURSEWORK
Data Structures • Algorithms • Software Engineering • Natural Language Processing • 
Database Systems • Web Development • C++ • Python

CERTIFICATIONS
Anthropic — Claude Code 101, AI Fluency and Frameworks, Building with Claude API & 
Introduction to MCP

LANGUAGES & TOOLS
Python • C++ • HTML • Figma • Salesforce • Claude Code & API • Cursor • Github • Jira

EXPERIENCE
Software Engineering Intern, Irenic Therapeutic | Jul 2025 – September 2025
• Designed and prototyped a patient connection platform inspired by matching algorithms
• Translated clinical and product requirements into mobile-first Figma wireframes
• Wrote Python scripts to automate design asset exports and streamlined documentation

Program Management Assistant, Arizona State University Workforce | Mar 2024 – Dec 2024
• Developed, tracked, and reported key performance metrics using Salesforce, Excel, and Jira
• Supported creation of communication and outreach materials

ACTIVITIES
Treasurer, CodeDevils (ASU)
• Managed and allocated club budget
• Maintained compliance with university regulations
"""

# ── Tracker file ──────────────────────────────────────────────────────────────
TRACKER_FILE = os.path.join(os.path.dirname(__file__), "applications.json")


def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return []


def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Subagent helper ───────────────────────────────────────────────────────────
def run_subagent(system_prompt: str, user_message: str) -> str:
    response = ai.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


# ── TOOLS ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def scrape_job(linkedin_url: str) -> str:
    """
    Scrape a LinkedIn job posting and return the job title, company, and description.

    Args:
        linkedin_url: Full LinkedIn job URL, e.g. https://www.linkedin.com/jobs/view/123456

    Returns:
        Job title, company name, and job description as plain text.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(linkedin_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1")
        company = soup.find("a", {"class": lambda c: c and "company" in c.lower()})
        description = soup.find("div", {"class": lambda c: c and "description" in c.lower()})

        title_text = title.get_text(strip=True) if title else "Unknown Title"
        company_text = company.get_text(strip=True) if company else "Unknown Company"
        desc_text = description.get_text(separator="\n", strip=True) if description else "No description found"

        return f"Title: {title_text}\nCompany: {company_text}\n\nDescription:\n{desc_text[:3000]}"
    except Exception as e:
        return f"Error scraping job: {str(e)}"


@mcp.tool()
def tailor_resume(job_description: str) -> str:
    """
    Use an AI subagent to tailor Ajay's resume to match a specific job description.

    Args:
        job_description: The full job description text

    Returns:
        A tailored version of the resume as plain text.
    """
    return run_subagent(
        system_prompt=(
            "You are an expert resume writer. Given a base resume and a job description, "
            "rewrite the resume to better match the role. Keep all facts accurate — do not "
            "invent experience. Emphasize relevant skills, reorder bullet points for impact, "
            "and adjust the summary to align with the job. Return only the resume text."
        ),
        user_message=(
            f"Here is my resume:\n{RESUME}\n\n"
            f"Here is the job description:\n{job_description}\n\n"
            "Please tailor my resume to this role."
        ),
    )


@mcp.tool()
def draft_cover_letter(job_title: str, company_name: str, job_description: str) -> str:
    """
    Use an AI subagent to write a personalized cover letter for a job.

    Args:
        job_title:       The title of the role
        company_name:    The name of the company
        job_description: The full job description text

    Returns:
        A cover letter as plain text.
    """
    return run_subagent(
        system_prompt=(
            "You are an expert cover letter writer. Write a concise, compelling cover letter "
            "for a CS internship applicant. Keep it to 3 paragraphs. Be specific to the role "
            "and company. Sound human and enthusiastic, not generic."
        ),
        user_message=(
            f"Write a cover letter for this role:\n"
            f"Job Title: {job_title}\n"
            f"Company: {company_name}\n"
            f"Job Description: {job_description}\n\n"
            f"Here is my resume for reference:\n{RESUME}"
        ),
    )


@mcp.tool()
def log_application(company: str, role: str, url: str, status: str = "Applied") -> str:
    """
    Log a job application to the local tracker.

    Args:
        company: Company name
        role:    Job title
        url:     Job posting URL
        status:  Application status (default: 'Applied')

    Returns:
        Confirmation message.
    """
    apps = load_tracker()
    apps.append({
        "company": company,
        "role": role,
        "url": url,
        "status": status,
        "date": datetime.now().strftime("%Y-%m-%d"),
    })
    save_tracker(apps)
    return f"Logged: {role} at {company} — Status: {status}"


@mcp.tool()
def view_applications() -> str:
    """
    View all logged job applications.

    Returns:
        A formatted list of all applications.
    """
    apps = load_tracker()
    if not apps:
        return "No applications logged yet."

    lines = []
    for i, app in enumerate(apps, 1):
        lines.append(
            f"{i}. {app['role']} at {app['company']} | {app['status']} | {app['date']}\n"
            f"   {app['url']}"
        )
    return "\n\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
