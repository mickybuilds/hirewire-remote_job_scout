<p align="center">
  <img src="docs/banner.webp" alt="HireWire — Remote Job Scout: an AI agent that searches, filters and tracks remote jobs" width="100%">
</p>

<p align="center">
  <a href="#-getting-started"><img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-2f5d50"></a>
  <img alt="Works with Claude, Codex, OpenCode, Antigravity" src="https://img.shields.io/badge/works%20with-Claude%20·%20Codex%20·%20OpenCode%20·%20Antigravity-7fc2a8">
  <img alt="No AI keys" src="https://img.shields.io/badge/AI%20keys-none-lightgrey">
</p>

<p align="center">
  <b>Find remote jobs you can <i>actually</i> take from your country, ranked against your real experience,<br>with a tailored ATS-ready CV for every one you pick.</b>
</p>

<p align="center">
  <a href="README.md">Español</a> · <b>English</b>
</p>

---

## 📋 Contents

- [🤔 Why HireWire](#-why-hirewire)
- [✨ How it works](#-how-it-works)
- [🖥️ The dashboard](#️-the-dashboard)
- [🚀 Getting started](#-getting-started) (about 10 minutes)
- [➕ Extra: add LinkedIn and Indeed](#-extra-add-linkedin-and-indeed) (optional)
- [🧭 Everyday use](#-everyday-use)
- [💸 What it costs](#-what-it-costs)
- [🔎 Job sources](#-job-sources)
- [🛡️ What makes it different](#️-what-makes-it-different)
- [🔒 Your privacy](#-your-privacy)
- [🧰 Troubleshooting](#-troubleshooting)
- [⚙️ Under the hood](#️-under-the-hood)
- [👩‍💻 Author](#-author)

---

## 🤔 Why HireWire

Job boards are full of "remote" roles that are not remote for you:

- ❌ "Remote — US only"
- ❌ "Work from anywhere"… and then *"must be authorized to work in the United States"* in the fine print
- ❌ Hybrid or on-site roles tagged as remote

If you live outside the US or Europe, you lose hours reading listings you could never take. And when a real match finally shows up, rewriting your CV takes another hour, with the temptation to stretch the truth.

**HireWire does the reading for you.** It only shows jobs that say, in their own words, that they are remote **and** open to where you live. Then it writes an honest CV built only from facts you confirmed.

> 🙋 **You stay in control.** HireWire never applies, never sends messages and never fills in forms. It finds, ranks and prepares. You decide and apply.

---

## ✨ How it works

<p align="center">
  <img src="docs/how-it-works.png" alt="HireWire workflow: install, profile, routes, search pipeline with free prefilter and AI classifier, local dashboard, tailored CV, you apply" width="100%">
</p>

<sub>Interactive version: download <a href="docs/how-it-works.html"><code>docs/how-it-works.html</code></a> and open it in your browser. Diagram made with <a href="https://github.com/tt-a1i/archify">Archify</a>.</sub>

| Step | You do | HireWire does |
| --- | --- | --- |
| **1. Profile** | Share your CV and answer a short interview (15–20 min). | Turns your experience into an **evidence bank**: each fact gets a code and a limit (what you did vs. what you took part in, tools you did *not* use). |
| **2. Routes** | Say where you live, where you can legally work and whether you accept hybrid. | Proposes 2–5 job families that fit your evidence and sets up the search: queries, filters and location rules made for **your** situation. |
| **3. Search** | Ask for a search whenever you want. | Pulls jobs from 5 free boards (and, if you want, LinkedIn and Indeed), drops duplicates and fake-remote listings for free, and has the AI read the most relevant ones: A / B / C priority, with the exact sentence that proves you can apply. |
| **4. CV** | Mark the jobs you like and press **CV in English** or **CV in Spanish**. | Re-checks the live listing and writes a **Harvard-format CV** (DOCX + PDF) using only facts from your evidence bank. |

---

## 🖥️ The dashboard

It runs on your computer at `http://localhost:8765`. Nothing is uploaded.

<p align="center">
  <img src="docs/dashboard.png" alt="HireWire dashboard with fictional sample jobs ranked A and B, each with location evidence, route and reason" width="100%">
</p>

<sub>Fictional sample data. You can try the demo yourself by opening <code>web/index.html</code> through any static server.</sub>

**Flow:** To review → Interested → CV ready → Applied. When you dismiss a job you pick a reason with one click ("sales or support", "not really remote"…), and the agent can use those reasons to tune future searches.

---

## 🚀 Getting started

> 💡 **You don't need any AI key or API key.** HireWire runs on the AI agent you already have: it uses your Claude, ChatGPT or Google plan, not a separate account. You don't need Apify to start either: searches use free job boards.

### What you need

1. **An AI agent.** See below for help choosing.
2. **Python 3.10 or newer.** You don't have to install it yourself: the agent checks it and, if it's missing, asks your permission to install it.

No programming knowledge is needed.

### Which agent should I use?

| Agent | How you use it | Works without paying? |
| --- | --- | --- |
| **Claude desktop app** (Code tab) · ⭐ recommended | Point and click, no terminal | No. Needs Claude Pro or a higher plan. |
| **[Antigravity](https://antigravity.google)** (Google) | Point and click, no terminal | Yes. Free plan with a Google account, with weekly limits. |
| **[Codex](https://openai.com/codex/)** (OpenAI) | Desktop app or terminal | Yes. Included in ChatGPT Free, with a small allowance. |
| **[OpenCode](https://opencode.ai)** | Terminal | Yes, with its free models (they rotate). |

**On a free plan** you can do the interview, run searches and get a few CVs, but you'll hit usage limits sooner. Ask the agent to classify fewer listings per search (for example, 20). Free models also make more mistakes: review the classifications and every CV more carefully before using them.

<sub>Plans as of September 2026. They change often: check each agent's pricing page.</sub>

### Recommended path: the Claude desktop app

All point and click, no terminal.

1. Download the app from **[claude.com/download](https://claude.com/download)** and sign in.
2. Open the **Code** tab and start a new session. When it asks for a folder, choose **Documents**.
3. Paste this sentence and send it:

   ```text
   Install HireWire from https://github.com/mickybuilds/hirewire-remote_job_scout following its INSTALL.md.
   ```

   The agent creates the `HireWire` folder, downloads the files and checks Python. If it needs to install anything, it asks your permission and explains what it does.
4. Start **another new session**, and this time choose the **Documents → HireWire** folder. This way the agent sees HireWire's instructions.
5. Type:

   ```text
   /hirewire
   ```

   From here the agent guides you: interview, routes, first search and dashboard.

<details>
<summary><b>Other options: Antigravity, Codex, OpenCode and terminal agents</b></summary>

<br>

With any agent, the process is the same:

1. Paste the install sentence above.
2. When it finishes, open the `HireWire` folder in the agent.
3. Type `/hirewire`, or *"start HireWire"* if your agent has no slash commands.

| Agent | How to open the `HireWire` folder |
| --- | --- |
| **Antigravity** (app) | Open the `HireWire` folder as the workspace. |
| **Codex** (app) | Choose the `HireWire` folder as the project. |
| **Claude Code** (terminal) | `cd` into the folder, then run `claude`. |
| **Codex** (terminal) | `cd` into the folder, then run `codex`. |
| **OpenCode** | `cd` into the folder, then run `opencode`. |
| **Antigravity CLI** | `cd` into the folder, then run `agy`. |
| **Gemini CLI** (paid Google AI plan) | `cd` into the folder, then run `gemini`. |

</details>

---

## ➕ Extra: add LinkedIn and Indeed

This is optional. The free boards are enough to start; add these later if you want more volume.

HireWire searches LinkedIn and Indeed through **Apify**, a service that gives USD 5 of free credit every month. An Indeed search costs cents and a LinkedIn search about USD 0.40. Every search has a spending cap, and the agent asks for your OK before spending credit.

1. **Create a free account.** Go to **[apify.com](https://apify.com)** and click **Sign up free**. You can sign up with Google, GitHub or an email address. No credit card is needed.
2. **Copy your token.** In the Apify Console: **Settings** (left menu) → **API & Integrations** tab → **Personal API tokens** → **copy** icon. The token starts with `apify_api_`.
3. **Save it yourself in the `.env` file.** Tell the agent: *"Open the .env file so I can paste my Apify token"*. It opens the file; paste the token right after the equals sign, save and close:

   ```text
   APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxxxxxxxxxx
   ```

   > ⚠️ **Don't paste the token into the agent's chat.** The token works like a password: it goes only in the `.env` file, which stays on your computer and is never uploaded. This way it never goes through the AI.

4. **Turn the sources on.** Tell the agent: *"Add Indeed and LinkedIn"*.

> ⚖️ **About LinkedIn.** Collecting data from LinkedIn goes against its terms of use, so HireWire leaves it off and asks you to confirm before turning it on. The Apify service reads public listings without using your LinkedIn account or password, but you use it at your own risk. If you'd rather not, you can turn on Indeed alone.

---

## 🧭 Everyday use

| You want to… | Say to your agent |
| --- | --- |
| Continue where you left off | `/hirewire` or *"what's next?"* |
| Run a new search | `/search` or *"search for jobs"* |
| Open the dashboard | *"open the dashboard"* |
| Get a CV for a job | Press **CV in English / CV in Spanish** on the dashboard and paste the copied request |
| Fix jobs that are not really remote or not open to your country | *"I'm seeing jobs that aren't remote"*: the agent finds the pattern and tightens the rules |
| Update your experience | `/profile` |
| Change job types, country or preferences | `/routes` |

If you added LinkedIn or Indeed, before every search with them the agent tells you the spending cap and waits for your OK.

---

## 💸 What it costs

| Item | Cost |
| --- | --- |
| HireWire | Free and open source (MIT) |
| Five free job boards | Free, no account |
| AI usage | Comes from your agent's plan, no separate keys. Each search classifies at most 60 listings by default, the most relevant ones, after the free filters. |
| Indeed (optional, via Apify) | ≈ USD 0.05 per full search |
| LinkedIn (optional, via Apify) | ≈ USD 0.40 per full search |
| Apify free plan | USD 5 of credit per month → several full searches |

Every Apify source has a hard spending cap (`max_spend_usd`), so a search can never go over it.

---

## 🔎 Job sources

| Source | Cost | Why it's there |
| --- | --- | --- |
| [Himalayas](https://himalayas.app) | free | Remote jobs filtered by your country |
| [Built In](https://builtin.com) | free | Remote jobs with the exact list of countries allowed to apply |
| [We Work Remotely](https://weworkremotely.com) | free | Paid postings, very little spam; region per job |
| [Remotive](https://remotive.com) | free | Curated remote jobs; region per job |
| [Jobicy](https://jobicy.com) | free | Remote jobs filtered by region |
| [Get on Board](https://www.getonbrd.com) | free, optional | Tech jobs in Latin America |
| Indeed (via Apify) | ≈ USD 0.05, optional | Extra volume from your national Indeed site |
| LinkedIn (via Apify) | ≈ USD 0.40, optional | The largest volume. Off by default: [read the note](#-extra-add-linkedin-and-indeed) |

Duplicates across sources are removed before the AI reads anything. After each search, the agent reports how many A and B jobs each source brought, so you can switch off the ones that don't pay off. Every job links to its original posting.

---

## 🛡️ What makes it different

- **🌎 Fake-remote detection, adapted to you.** A job is *eligible* only with two quotes from the listing: one proving it is remote and one proving it is open to where you live or can legally work. "Remote" alone is marked *unclear*. When a listing names no country, the AI reads it whole for clues ("401(k)" or "US medical plan" point to US-only; "we hire through Deel" points to international).
- **🧾 Evidence bank against invented CVs.** Every CV line must trace back to a confirmed fact, and every fact carries its own limits. Participation is never turned into leadership.
- **📄 Harvard-format CVs without AI filler.** One column, standard headings, right-aligned dates, readable by ATS filters. A banned-phrase list keeps out "passionate", "results-driven", "spearheaded" and the like.
- **💰 Cheap by design.** Free filters remove most of the noise before the AI reads anything: in real use, ~60 % of irrelevant listings with zero good jobs lost.
- **🧠 Prompt-injection aware.** Job listings are treated as data. Hidden instructions inside a listing are ignored and flagged.
- **🌐 Bilingual.** Interview, dashboard and CVs in English or Spanish.
- **📦 Zero dependencies.** Python standard library only, including the DOCX generator.

### 📊 First real run

Built for and tested by a legal professional in Argentina looking for remote work with foreign employers:

- ~1,100 listings fetched in the first search → 750 unique after removing duplicates
- 27 A/B matches, each with the eligibility sentence quoted
- **USD 0.36** of Apify credit, with a USD 1 cap

---

## 🔒 Your privacy

Everything personal stays on your computer and is excluded from Git:

| Folder / file | What it holds |
| --- | --- |
| `profile/` | Your CV, evidence bank, routes and search settings |
| `data/` | Job listings, classifications, your statuses and notes |
| `applications/` | Your tailored CVs |
| `.env` | Your Apify token, if you added LinkedIn or Indeed |

HireWire has no server and no analytics. The only outside calls are the job sources you enable and your own AI agent.

---

## 🧰 Troubleshooting

<details>
<summary><b>"python is not recognized" / Python not found</b></summary>

Ask your agent to install Python 3.10+. On Windows it can use `winget install Python.Python.3.12`; on macOS, `brew install python`. On macOS and Linux the command may be `python3` instead of `python`, and HireWire's instructions already account for it.
</details>

<details>
<summary><b><code>/hirewire</code> does nothing or is "unknown"</b></summary>

The agent must be running **inside** the HireWire folder (see step 4 of the recommended path). In agents without slash commands, write "start HireWire" instead.
</details>

<details>
<summary><b>I ran out of my free plan's limit, or a search uses too much</b></summary>

Tell the agent: *"classify only 20 listings per search"*. The rest wait for the next search. Free plan limits reset on their own (daily or weekly, depending on the agent).
</details>

<details>
<summary><b>The dashboard doesn't open</b></summary>

Another program may be using port 8765. Ask the agent to open the dashboard on another port (8766).
</details>

<details>
<summary><b>I see jobs that are on-site, hybrid or not open to my country</b></summary>

Tell your agent, with one or two examples. It finds why they got through, tightens the rule, checks that no good job is lost and cleans the dashboard.
</details>

<details>
<summary><b>"APIFY_TOKEN missing in .env"</b> (only if you added LinkedIn or Indeed)</summary>

Check that the file is named exactly `.env` (not `.env.txt`), that it is in the HireWire folder, and that the line reads `APIFY_TOKEN=` followed by your token with no spaces.
</details>

<details>
<summary><b>My Apify credit ran out</b></summary>

Searches keep running with the five free sources. Apify renews the free credit every month.
</details>

---

## ⚙️ Under the hood

<details>
<summary><b>Search pipeline</b></summary>

1. `fetch` queries each enabled source, removes duplicates (canonical URL and company + title) and applies free filters: excluded companies, residence or work-permit requirements for other countries, on-site or hybrid listings that never say "remote", unrelated job titles and old listings.
2. `batch` ranks the pending listings by relevance (title match, domain terms, date) and splits the top ones into batches.
3. One AI subagent per batch applies `config/criteria.md` with your profile and writes one JSON line per listing.
4. `merge` validates every line (allowed values, your route ids, a location quote for every *eligible* job) and reports errors for a retry.
5. `sources` and `test-prefilter` measure each source's yield and replay the filters against past classifications, so rules can be tuned without losing good jobs.
</details>

<details>
<summary><b>Project structure</b></summary>

```text
.claude/skills/        entry point and the four stages (/hirewire, /profile, /routes, /search, /cv)
AGENTS.md              instructions for any agent (CLAUDE.md and GEMINI.md import it)
.agents/               rule and skills for Antigravity (they point to AGENTS.md and .claude/skills)
INSTALL.md             installation steps the agent follows
config/criteria.md     classification rules: location, route, level, priority, output format
config/cv_style.md     CV format and writing rules
templates/             starting point for your profile files
scripts/hirewire.py    pipeline: check, fetch, batch, merge, status, sources, refilter, test-prefilter
scripts/dashboard.py   local dashboard server
scripts/make_docx.py   Markdown → Harvard-format DOCX and PDF
web/                   dashboard (local and demo mode)
docs/                  images and the interactive diagram

profile/  data/  applications/  .env     your private data, ignored by Git
```
</details>

<details>
<summary><b>Commands</b></summary>

```bash
python scripts/hirewire.py check          # validate your profile folder
python scripts/hirewire.py fetch          # free sources only
python scripts/hirewire.py fetch --with-apify   # also LinkedIn and Indeed, if enabled (spends Apify credit)
python scripts/hirewire.py batch          # prepare the most relevant listings for the AI
python scripts/hirewire.py merge          # validate and store the AI results
python scripts/hirewire.py status         # where you are and what's next
python scripts/hirewire.py sources        # A/B/C yield per source
python scripts/dashboard.py               # open the dashboard at http://localhost:8765
```

You rarely need these: the agent runs them for you.
</details>

---

## 👩‍💻 Author

Made by **Micaela D. Asquini**, a tech lawyer who loves building things: AI legal solutions, legal ops and legal tech. HireWire began as her own job search.

## 📄 License

[MIT](LICENSE). Job listings belong to their publishers; HireWire links to the original postings and does not republish them.
