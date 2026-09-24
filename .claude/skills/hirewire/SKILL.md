---
name: hirewire
description: Entry point of HireWire. Checks where the user is in the workflow (profile, routes, search, CV) and continues from there. Use when the user says "hirewire", "start", "empezar", "seguir", "¿qué sigue?", or opens the project without a specific request.
---

# HireWire — what's next

Run:

```
python scripts/hirewire.py status
```

(Use `python3` or `py` if `python` is not available.)

Act on `next_stage`:

| `next_stage` | What to do |
| --- | --- |
| `profile` | New user. Explain HireWire in three lines: (1) a short interview builds your evidence bank from your CV, (2) you choose job routes and where you can work, (3) searches fill a local dashboard ranked for you, (4) you pick jobs and get a tailored CV for each. You apply yourself. Then start the profile workflow. |
| `routes` | Say the profile is ready and start the routes workflow. |
| `search` | Say everything is set up and start the search workflow. |
| `classify` | There are listings fetched but not classified. Offer to classify them (search workflow, from step 2). |
| `cv` | `interested_without_cv` jobs are waiting for a CV. List them (title and company, from `data/jobs.jsonl`) and ask which ones and in which language, then follow the CV workflow. |
| `review` | Everything is up to date. Show `by_priority` and `last_search`, and offer: a new search, opening the dashboard, a CV for a job, updating the profile, or fixing location rules if non-eligible jobs show up. |

If `profile/EVIDENCE.md` looks unfinished (many facts under "Unconfirmed", skills section empty), offer to resume the interview before moving on.

Workflows:
- Profile: `.claude/skills/profile/SKILL.md`
- Routes: `.claude/skills/routes/SKILL.md`
- Search: `.claude/skills/search/SKILL.md`
- CV: `.claude/skills/cv/SKILL.md`
