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

## 4. Apify account

Explain: HireWire searches LinkedIn and Indeed through Apify, besides five free job boards. A free Apify account gives USD 5 of credit per month, enough for several full searches; each search has a spending cap. Without it, HireWire still works with free sources, but finds fewer jobs.

If the user wants it now:
1. They create a free account at https://apify.com and copy the API token from Settings → API & Integrations.
2. Copy `.env.example` to `.env` in the HireWire folder and open it for them. They paste the token after `APIFY_TOKEN=` and save. Never ask them to paste the token in the chat.

They can also do this later, during the routes stage.

## 5. Open the project

The HireWire workflows load when the agent runs inside the HireWire folder. Tell the user how to continue with their tool:
- Claude Code (desktop app): open a new session and choose the HireWire folder. Terminal: `cd "<folder>"` and `claude`.
- Codex, OpenCode, Gemini CLI or another agent: start it inside the HireWire folder.

Then they type `/hirewire` (or write "start HireWire") and the interview begins.
