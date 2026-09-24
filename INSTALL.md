# Installing HireWire

Instructions for the AI agent that installs HireWire for a user. Speak in the user's language and explain each step in one short line. Ask before installing any software.

## 1. Choose the folder

Ask where to install it. Suggest a `HireWire` folder inside the user's Documents folder. It must not be inside a cloud-synced folder that the user shares with others.

## 2. Get the files

- If `git` is available: `git clone https://github.com/mickybuilds/hirewire-remote_job_scout.git "<folder>"`.
- Otherwise, download and extract the ZIP:
  - Windows (PowerShell): `Invoke-WebRequest https://github.com/mickybuilds/hirewire-remote_job_scout/archive/refs/heads/main.zip -OutFile hirewire.zip; Expand-Archive hirewire.zip -DestinationPath "<parent folder>"`, then rename `hirewire-remote_job_scout-main` to the chosen folder name.
  - macOS / Linux: `curl -L -o hirewire.zip https://github.com/mickybuilds/hirewire-remote_job_scout/archive/refs/heads/main.zip && unzip hirewire.zip`, then rename the folder the same way.

## 3. Check Python

HireWire needs Python 3.10 or newer, with no extra packages. Try `python --version`, `python3 --version` and, on Windows, `py --version`.

If none works or the version is older, ask the user for permission and install it:
- Windows: `winget install Python.Python.3.12`, or the installer from python.org (check "Add python.exe to PATH").
- macOS: `brew install python`, or the installer from python.org.
- Linux: the distribution's package manager (`sudo apt install python3`).

## 4. Open the project

HireWire needs no AI key or API key: it runs on the user's own agent plan. The first searches use free job boards only. LinkedIn and Indeed (through Apify) are an optional extra the user can add later; do not bring it up now.

The HireWire workflows load when the agent runs inside the HireWire folder. Tell the user how to continue with their tool:
- Claude desktop app (Code tab): start a new session and choose the HireWire folder.
- Antigravity (app): open the HireWire folder as the workspace.
- Terminal agents (Claude Code, Codex, OpenCode, Antigravity CLI, Gemini CLI): `cd "<folder>"` and start the agent there.

Then they type `/hirewire` (or write "start HireWire") and the interview begins.
