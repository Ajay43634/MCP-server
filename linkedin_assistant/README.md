# 🔗 LinkedIn Job Assistant — MCP Server

A Python MCP server that plugs directly into **Claude Desktop** and turns it into a personal job-hunting assistant. Point it at a LinkedIn posting and Claude can scrape it, tailor your resume, write a cover letter, and log the application — all in one conversation.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| `scrape_job` | Scrapes a LinkedIn job posting and extracts the title, company, and description |
| `tailor_resume` | Uses a Claude AI subagent to rewrite your resume for a specific job |
| `draft_cover_letter` | Uses a Claude AI subagent to write a 3-paragraph personalized cover letter |
| `log_application` | Saves a job application (company, role, URL, status) to a local JSON tracker |
| `view_applications` | Displays all tracked applications in a formatted list |

---

## 🛠️ Built With

- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [Anthropic Python SDK](https://github.com/anthropic/anthropic-sdk-python) — Claude AI subagents
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — LinkedIn job scraping
- [python-dotenv](https://github.com/theskumar/python-dotenv) — API key management

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/Ajay43634/MCP-server.git
cd MCP-server/linkedin_assistant

# 2. Install dependencies
pip install anthropic fastmcp beautifulsoup4 requests python-dotenv

# 3. Create a .env file with your Anthropic API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

---

## ⚙️ Claude Desktop Setup

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linkedin-assistant": {
      "command": "python3",
      "args": ["/path/to/MCP-server/linkedin_assistant/server.py"]
    }
  }
}
```

Then restart Claude Desktop.

---

## 🚀 Usage

Once connected, ask Claude things like:

> *"Scrape this LinkedIn job and tailor my resume to it: https://linkedin.com/jobs/view/..."*

> *"Draft a cover letter for the ML Engineer role at Google."*

> *"Log my application to Anthropic for the Research Engineer position."*

> *"Show me all the jobs I've applied to."*

---

## 📁 Project Structure

```
linkedin_assistant/
├── server.py          # MCP server with all tools
├── applications.json  # Auto-generated application tracker
└── .env               # API key (not committed)
```

---

## 🔒 Notes

- Your resume is baked into `server.py` — update the `RESUME` constant with your own
- `applications.json` is created automatically on first use
- Never commit your `.env` file — add it to `.gitignore`

---

## 👤 Author

**Ajay Rao** — CS @ San Diego State University
