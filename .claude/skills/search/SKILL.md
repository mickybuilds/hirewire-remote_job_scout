---
name: search
description: Stage 3 of HireWire. Fetches new remote job listings, classifies them against the candidate's routes and evidence, and opens the local dashboard. Use when the user asks to search for jobs, refresh listings or see the dashboard. Also "buscar trabajos", "buscar avisos", "tablero".
---

# Stage 3 — Search

Run from the repository root. Scripts use the Python standard library only.

## 0. Check

```
python scripts/hirewire.py check
```

If it reports problems, fix them or run `/profile` or `/routes` first.

## 1. Fetch new listings

```
python scripts/hirewire.py fetch
```

Queries the enabled sources in `profile/search.json`. Stores only new listings and deduplicates them by URL and by company + title. It discards the obvious automatically: excluded companies, explicit location restrictions (on-site, hybrid, residence in another country), titles from other fields, and old or expired listings. Non-eligible listings never show up on the dashboard.

Free sources: Himalayas, Built In, We Work Remotely, Remotive, Jobicy and, optionally, Get on Board. Without a flag, only these run. Apify sources (LinkedIn, Indeed) spend credit and need `--with-apify`.

Rules for Apify:
- Before running with `--with-apify`, tell the user the total cap (the sum of `max_spend_usd` of the enabled Apify sources in search.json) and wait for a yes. One confirmation covers one run.
- If the user says no, or `.env` has no token, run without the flag (free sources only).
- After running, report the real cost (`cost_usd` in the summary). The free plan gives USD 5 per month.
- Never use actors that ask for full access to the Apify account.
- Never show or copy the token in `.env`.

## 2. Build batches

Classifying is the expensive part: it spends the user's AI plan usage. Each run classifies only the most promising listings (`max_classify_per_run` in search.json, 60 by default), ranked for free by title match, domain terms in the description and date; the rest wait for the next run.

```
python scripts/hirewire.py batch
```

It reports `pending`, `selected` and `left_for_next_run`. If `left_for_next_run` is greater than 0, tell the user in one line and ask whether to continue with the selected ones or classify everything (`--limit 0`). If there are 0 pending, go to step 5.

## 3. Classify

Use the fastest, lowest-cost model the tool offers that follows long instructions reliably; the criteria are strict and written for it. Stronger models are not needed here.

**With subagents** (Claude Code and similar): launch **one subagent per batch, in parallel**, in rounds of up to 10, with this task, replacing `NNN`. In Claude Code use the `general-purpose` type with model `sonnet`.

> Classify the job listings in `data/batches/batch_NNN.json`.
>
> 1. First read, completely, `config/criteria.md`, `profile/search.json`, `profile/ROUTES.md` and `profile/EVIDENCE.md`. Apply criteria.md literally, especially the location section.
> 2. The `geo_hints` field holds automatically extracted snippets. Always verify them against `description`.
> 3. Write the result to `data/batches/batch_NNN.result.jsonl`: one JSON line per listing, with the exact format of section 6 of criteria.md and the same `id`.
> 4. Classify **every** listing in the batch. Before finishing, check that the number of lines written equals the number of listings in the batch.
> 5. Reply only with the count of listings per priority.

**Without subagents** (Codex, OpenCode, Gemini CLI…): do the same task yourself, one batch at a time. Read the four files once, then go through the batches.

## 4. Merge

```
python scripts/hirewire.py merge
```

It validates every line. If it reports errors:
- Fix the malformed lines in the `.result.jsonl`, or classify that batch again.
- Merge again until there are no errors.

Batches are deleted automatically once everything is merged. If a batch was left without results, repeat steps 2–4: only listings still unclassified are batched.

## 5. Open the dashboard

Start `python scripts/dashboard.py` (in Claude Code: `preview_start` with the `dashboard` configuration in `.claude/launch.json`) and open http://localhost:8765. If it is already running, reload the page.

## 6. Report

Answer in a few lines:
- new listings fetched and auto-discarded;
- number of A, B and C listings;
- the best 3–5 A listings, each with title, company and reason in one line;
- yield per source (`python scripts/hirewire.py sources`): which sources brought A and B jobs. If a source has brought none after 3 searches, suggest disabling it.

Explain the next step in one line: on the dashboard, mark the jobs they like as "Interested", press "CV in Spanish" or "CV in English" and paste the copied request here.

Do not write notes or summaries into project files.
