---
name: cv
description: Stage 4 of HireWire. Writes a tailored Harvard-format, ATS-friendly CV (DOCX and PDF) in Spanish or English for a job the user marked "Interested" on the dashboard. Use when the user asks for a CV for a listing, or pastes a dashboard request like "HireWire: write the CV in English for job <id>" / "HireWire: armá el CV en español para el aviso <id>".
---

# Stage 4 — Tailored CV

The user applies on their own. The agent never submits applications or fills in forms.

## 1. Pick the listing and the language

- If the message has a job id (the dashboard's "CV in Spanish / CV in English" buttons copy one), use it.
- Otherwise read `data/statuses.json`, find listings with `status: interested` and no CV yet (no `applications/*/meta.json` with that `job_id`), and ask which one.
- **Language:** the one in the request. If it was not given, ask: Spanish or English. Suggest the language of the listing.
- Take the data from `data/jobs.jsonl` and `data/classification.jsonl`.

## 2. Verify the original listing

- Open the listing URL with the web fetch tool. If there is an application URL, open it too.
- Confirm:
  1. it is still open;
  2. it is eligible from the candidate's country, quoting the exact sentence;
  3. any requested CV format (PDF, page limit, language).
- If it closed or does not accept the candidate's country, tell the user and stop.

## 3. Create the folder

`applications/YYYY-MM-DD_company_role/`, lowercase, words joined with hyphens. If a CV in another language already exists for the same job, reuse the folder and add the language to the file name.

Files:
- `meta.json`: `{"job_id": "<id>", "language": "es|en", "created": "YYYY-MM-DD"}`. The dashboard uses it to show "CV ready" and the download buttons.
- `listing.md`: title, company, URL, verification date and full text of the listing.
- `analysis.md`:
  - a table with each requirement (mandatory or nice to have), the `E-...` code that backs it and its status: meets, transferable, gap or unsupported;
  - the route and CV angle chosen from `profile/ROUTES.md`;
  - questions for the user if a fact is missing.
- `cv.md`: the CV in the format of `config/cv_style.md`.
- `CV_<Name>_<Company>.docx` and `.pdf`.

## 4. Write the CV

Read `config/cv_style.md` and follow it exactly: Harvard format, section order, writing rules and forbidden words.

- Facts come **only** from `profile/EVIDENCE.md`. Respect every **Limit**. Never use anything under "Unconfirmed".
- One target role per CV. Open each role with the bullets that prove the listing's main requirements.
- Translate facts faithfully into the CV language; do not add meaning while translating.

## 5. Generate and check

```
python scripts/make_docx.py <folder>/cv.md <folder>/CV_<Name>_<Company>.docx --pdf
```

If the PDF could not be created, tell the user to open the .docx and export it as PDF (Word, LibreOffice or Google Docs).

Then:
- Run the "Final check" of `config/cv_style.md` line by line.
- Run `python scripts/docx_text.py <folder>/CV_<Name>_<Company>.docx` and check that order and contact details read correctly.

## 6. Deliver

Tell the user, briefly:
- the CV is ready on the dashboard, under "CV ready", with the download buttons (reload the page);
- the chosen angle;
- the 2–3 main gaps;
- pending questions, if any.

In Claude Code, also send the PDF with `SendUserFile`.
