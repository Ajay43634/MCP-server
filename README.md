# 🔗 MCP LinkedIn Server

A Python-based **Model Context Protocol (MCP)** server that integrates LinkedIn functionality directly into AI assistants like Claude Desktop. This allows you to interact with LinkedIn programmatically through natural language.

## Features

- 🤖 Connects LinkedIn to Claude Desktop via MCP
- 📄 Scrape and read LinkedIn job postings
- 📝 Tailor resumes and draft cover letters based on job descriptions
- 📊 Track and log job applications
- 💼 View and manage application history

## Tech Stack

- **Python** — core server logic
- **MCP (Model Context Protocol)** — connects the server to Claude Desktop
- **LinkedIn Assistant Tools** — job scraping, resume tailoring, cover letter drafting, application tracking

## Setup

### Prerequisites

- Python 3.10+
- Claude Desktop installed
- LinkedIn account

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ajay43634/MCP_Linkedin_Server.git
cd MCP_Linkedin_Server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Claude Desktop by adding the following to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "linkedin-assistant": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

4. Restart Claude Desktop — the LinkedIn tools will be available automatically.

## Usage

Once connected, you can ask Claude things like:

- *"Scrape this LinkedIn job posting and tailor my resume for it"*
- *"Draft a cover letter for this job"*
- *"Log this application to my tracker"*
- *"Show me all the jobs I've applied to"*

## Project Structure

```
MCP_Linkedin_Server/
├── server.py          # Main MCP server
├── requirements.txt   # Python dependencies
└── README.md
```

## Author

**Ajay Rao** — CS Student at San Diego State University  
[GitHub](https://github.com/Ajay43634)
