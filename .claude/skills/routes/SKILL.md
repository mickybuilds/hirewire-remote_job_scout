---
name: routes
description: Stage 2 of HireWire. Turns the evidence bank into search routes (profile/ROUTES.md) and the search configuration (profile/search.json), adapted to where the candidate lives and can legally work. Use after /profile, when the user wants to change what jobs to look for, their country or preferences, or when they complain that listings are not remote or not open to their country. Also "rutas", "configurar la búsqueda", "me aparecen trabajos presenciales", "no son para mi país".
---

# Stage 2 — Routes and search configuration

Requires `profile/EVIDENCE.md`. If it does not exist, run `/profile` first.

Outputs:
- `profile/ROUTES.md`: what to look for and how to present the candidate for each route.
- `profile/search.json`: location rules, preferences, sources, queries and prefilter.

Speak in the user's language. If `profile/search.json` already exists and the user only wants to fix location problems, go to step 6.

## 1. Where the candidate can work

This is the most important part: a listing the candidate cannot take is noise, however good the fit. Ask one or two questions at a time and explain why when it helps.

1. **Residence:** country and city. Derive `country_code` (ISO 3166-1 alpha-2) and `utc_offset`.
2. **Work authorization:** "Besides {country}, can you legally work anywhere else? For example a second citizenship, an EU passport, a work visa or a green card." Record every country or bloc in `work_authorization`, starting with the country of residence. Explain the difference: authorization opens jobs that ask for the right to work there, but not jobs that require living there.
3. **Work mode:** remote only, or also hybrid or on-site in their city (`remote_only` or `remote_or_hybrid`).
4. **Regions:** which region names include them in listings ("LATAM", "Latin America", "Americas", "EMEA", "Europe", "APAC"…). Propose the list and confirm it.
5. **Time zones:** can they work a foreign schedule (for example US Eastern hours)? This only changes alerts, never eligibility.

Then summarize the rule in one sentence and confirm it. Example: "You will only see jobs that say they are remote and are open to Mexico, LATAM, the Americas or anywhere. Jobs that ask for the right to work in the EU also count, because of your Spanish passport; jobs that require living in Europe do not."

## 2. Other preferences

1. Contract preference: contractor, employee or either.
2. Local employers: same priority as foreign ones, or lower.
3. Working languages.
4. Companies or kinds of jobs they never want to see (for example pay-per-task AI training platforms).
5. Language for the dashboard and classifier notes (`en` or `es`).

## 3. Propose routes

Read EVIDENCE.md completely. Group the facts into 2–5 routes: a family of jobs the evidence can credibly support. Include at least one adjacent or transition route if the evidence allows it, marked with a lower level.

For each route, fill the structure of `templates/ROUTES.md`:
- target work, typical titles (the words real listings use, in English and in the local language when relevant);
- level, and when to aim lower;
- CV angles: which `E-` codes open the CV, and 6–9 skills backed by evidence;
- typical gaps, what is out of route, what must not be claimed.

Present the routes to the user briefly and adjust them together. Routes with weak evidence can be kept as postponed (classified `C`).

## 4. Write the files

1. `profile/ROUTES.md` from `templates/ROUTES.md`. Only operative criteria, no conversation notes.
2. `profile/search.json` from `templates/search.json`:
   - `language` and `candidate` from steps 1 and 2. `local_employers`: `lower_priority` or `same`.
   - `routes`: `{"route_id": "Short label"}` for every route, postponed ones included. Ids in lowercase, no spaces.
   - `sources.himalayas.queries`: 12–25 short English queries covering the titles of all routes. Short queries find more.
   - `sources.apify_linkedin` and `sources.apify_indeed`: write their queries now but leave `enabled` as `false`. They are turned on only through step 7.
   - `sources.apify_linkedin`: `location` = the country name in English; `geo_id` from the table below, or empty if the country is not listed. 10–16 queries: the most specific titles, plus 2–3 in the local language if it is not English.
   - `sources.apify_indeed`: searches the candidate's national Indeed site (`country` empty = `country_code`). 8–12 short queries, mixing English and the local language; broad ones work because the prefilter drops non-remote listings.
   - `sources.builtin`: `country` = ISO 3166-1 alpha-3 code of the country of residence (`ARG`, `MEX`, `USA`); 6–10 short queries.
   - `sources.jobicy`: `geo` = the region slug that contains the candidate (`latam`, `usa`, `canada`, `emea`, `europe`, `apac`); 4–6 short queries.
   - `sources.weworkremotely` and `sources.remotive` need no queries: they read the whole recent feed and the prefilter keeps what fits.
   - `sources.getonboard`: tech jobs in Latin America. Enable it only for candidates in Latin America with technical routes.
   - `prefilter.route_title_terms`: word stems that appear in titles of every route, both languages.
   - `prefilter.description_signals`: 25–45 domain terms that show a listing is related even when the title is not.
   - `prefilter.foreign_title_terms`: common titles of unrelated fields. Remove any that overlaps a route.
   - `prefilter.excluded_companies`: from step 2.
   - Location rules, see step 5.
3. Run `python scripts/hirewire.py check` and fix what it reports.

LinkedIn `geo_id` for common countries: Argentina 100446943, Brazil 106057199, Chile 104621616, Colombia 100876405, Mexico 103323778, Peru 102927786, Uruguay 100867946, Spain 105646813, United States 103644278, Canada 101174742, United Kingdom 101165590.

## 5. Location rules in the prefilter

The prefilter discards obvious non-eligible listings for free, before the classifier reads them. Adapt the template to the candidate:

All patterns are regular expressions over the normalized text (lowercase, no accents).

- `geo_exclusions` (always applied):
  - Work-authorization patterns ("authorized to work in…", "sponsorship"): remove the ones that name an authorized country or bloc. Someone with an EU passport removes the EU ones.
  - Residence patterns ("must be based in…", "…residents only", "remote - …"): remove only the ones that name the country of residence or a region that contains it. A passport does not meet a residence requirement: a Spanish citizen living in Mexico keeps "must be based in Europe".
  - Add the equivalent patterns for large markets that are not authorized and not in the template, if the candidate's routes point there (for example Germany, Australia).
- `mode_exclusions` (hybrid, on-site, in office): applied only when the listing never says it is remote and does not come from a `remote_only_sources` board, because companies mention offices and hybrid teams in boilerplate. If `work_mode` is `remote_or_hybrid`, leave the list empty.
- `remote_only_sources`: boards that only publish remote jobs (keep the template list).
- `remote_required_sources`: sources whose "remote" filter is unreliable (`LinkedIn`, `Indeed`). A listing from these sources that never says it is remote is discarded. Leave it empty if `work_mode` is `remote_or_hybrid`.
- `remote_signals`: add the local-language ways of saying "remote" if the country's language is not English or Spanish.

Every rule must be safe: if in doubt, leave the listing for the classifier.

## 6. Tuning location rules later

When the user says they see jobs that are not remote or not open to them (or the dashboard shows many dismissals with reason `not_remote`):

1. Ask for one or two examples, or read the dismissed jobs with that reason from `data/statuses.json` and `data/jobs.jsonl`.
2. Find why each one got through: a phrase the rules do not catch, a source whose remote filter failed, or a classifier mistake.
3. Change the smallest thing that fixes it: a pattern in `geo_exclusions`, a source in `remote_required_sources`, or a rule in `candidate`. Rewrite in place.
4. Run `python scripts/hirewire.py test-prefilter`: `good_jobs_lost` must stay empty. If the change removes good jobs, make it narrower.
5. Run `python scripts/hirewire.py refilter --location` to apply the new rules to the jobs already on the dashboard.
6. Tell the user how many jobs were removed and show two or three examples.

## 7. Optional: LinkedIn and Indeed through Apify

Only when the user asks for it, or after the first searches if they want more volume. Never as part of the first setup: HireWire works with the free boards alone.

Apify gives USD 5 of free credit per month. Indeed costs cents per search; LinkedIn about USD 0.40. Each source has a hard cap in `max_spend_usd`.

1. The user creates a free account at apify.com and copies the API token from Settings → API & Integrations.
2. If `.env` does not exist, copy `.env.example` to `.env`. Open `.env` for the user in their editor or file viewer. They paste the token after `APIFY_TOKEN=`, save and close. Tell them not to paste the token in the conversation. Never read the file.
3. Enable `sources.apify_indeed`.
4. LinkedIn: before enabling `sources.apify_linkedin`, tell the user that collecting data from LinkedIn goes against LinkedIn's terms of use. The Apify actor reads public listings and does not use their LinkedIn account or password, but they use it at their own risk. Enable it only if they say yes.

## 8. Next step

Tell the user the location rule in one sentence, the routes, and the number of queries per source. Suggest `/search`.
