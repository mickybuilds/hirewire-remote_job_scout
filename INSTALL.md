# Installing HireWire

Instructions for the AI agent that installs HireWire for a user. Speak in the user's language and explain each step in one short line. Ask before installing any software.

## 1. Choose the folder

Do not ask; decide and say where in one line:
- If the current folder is empty, or is named `HireWire` and holds nothing but hidden files, install there.
- Otherwise, install in a new `HireWire` folder inside the current one. If that already exists and is not empty, ask.

Never install inside a cloud-synced folder that the user shares with others.

## 2. Get the files

- If `git` is available: `git clone https://github.com/mickybuilds/hirewire-remote_job_scout.git "<folder>"` (use `.` as the folder when installing in the current one).
- Otherwise, download and extract the ZIP:
  - Windows (PowerShell): `Invoke-WebRequest https://github.com/mickybuilds/hirewire-remote_job_scout/archive/refs/heads/main.zip -OutFile hirewire.zip; Expand-Archive hirewire.zip -DestinationPath "<parent folder>"`, then rename `hirewire-remote_job_scout-main` to the chosen folder name.
  - macOS / Linux: `curl -L -o hirewire.zip https://github.com/mickybuilds/hirewire-remote_job_scout/archive/refs/heads/main.zip && unzip hirewire.zip`, then rename the folder the same way.

## 3. Check Python

HireWire needs Python 3.10 or newer, with no extra packages. Try `python --version`, `python3 --version` and, on Windows, `py --version`.

If none works or the version is older, ask the user for permission and install it:
- Windows: `winget install Python.Python.3.12`, or the installer from python.org (check "Add python.exe to PATH").
- macOS: `brew install python`, or the installer from python.org.
- Linux: the distribution's package manager (`sudo apt install python3`).

## 4. Continue in this session

HireWire needs no AI key or API key: it runs on the user's own agent plan. The first searches use free job boards only. LinkedIn and Indeed (through Apify) are an optional extra the user can add later; do not bring it up now.

Tell the user in one or two lines that HireWire is installed, where, and that you are starting now. Then, without asking them to reopen anything:
1. Read `<folder>/AGENTS.md` and follow it for the rest of this session. Every path in it and in the workflows is relative to `<folder>`; run commands from there.
2. Follow the entry point workflow (`<folder>/.claude/skills/hirewire/SKILL.md`).

In this first session, slash commands such as `/profile` or `/search` may not work, because the agent was started outside the folder. Accept the same requests in words ("next", "search for jobs").

At the end of this session, or if the user stops, tell them once how to open HireWire next time, so slash commands work:
- Claude desktop app (Code tab): start a new session and choose the HireWire folder.
- Antigravity (app): open the HireWire folder as the workspace.
- Terminal agents (Claude Code, Codex, OpenCode, Antigravity CLI, Gemini CLI): `cd "<folder>"` and start the agent there.

Then they type `/hirewire` (or write "start HireWire") and continue where they left off.
