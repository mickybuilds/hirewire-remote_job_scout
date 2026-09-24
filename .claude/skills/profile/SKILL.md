---
name: profile
description: Stage 1 of HireWire. Builds the candidate's evidence bank (profile/EVIDENCE.md) from their CV and a short, targeted interview. Use when the user starts HireWire, wants to create or update their profile, or says "perfil", "entrevista", "analizá mi CV".
---

# Stage 1 — Profile and evidence bank

Output: `profile/EVIDENCE.md`, the single source of facts for every later stage. A fact that is not there never reaches a CV.

Speak in the user's language. Write EVIDENCE.md in that language, except for role titles as they appear on the CV.

The interview should take 15–20 minutes: about 10–15 questions. Every question must earn its place: ask only what the CV does not already answer well.

## 1. CV first

Ask: "Do you have a CV? Drop it in `profile/sources/` (create the folder) or paste it here. A LinkedIn export or portfolio also helps." None is mandatory.
- PDF: read it with the Read tool.
- DOCX: `python scripts/docx_text.py <file>`.
- No CV: start the interview from the most recent job.

If `profile/EVIDENCE.md` already exists, this is an update or a resumed interview: read it, say what is already covered, and continue from what is missing.

## 2. Read and plan

From the CV, list privately for each role: organization, title, dates, contract type, remote or on-site, and the claims it makes. Mark:
- **solid**: action + context + result are clear;
- **vague**: "responsible for", "helped with", "managed", with no concrete deliverable;
- **inflated or unverifiable**: numbers, leadership, "expert".

Then write a first `profile/EVIDENCE.md` from `templates/EVIDENCE.md` with the solid facts, and the rest under "Unconfirmed". Tell the user: "I read your CV. I have N roles; I want to confirm or sharpen X points. It takes about 15 minutes, and you can stop and continue later."

## 3. Interview in blocks

One question at a time, two at most when closely related. After each block, update EVIDENCE.md (move confirmed facts out of "Unconfirmed"), so nothing is lost if the session ends.

**Block A — Recent and relevant roles** (4–6 questions). Only for vague or inflated claims, and for roles with few facts.
- Story questions, which reveal skills people do not list:
  - "Tell me about one specific case where you [claim]. What was the situation, what did you do, what happened next?"
  - "What did you build or change that did not exist before you arrived? Who used it afterwards?"
  - "What problem did you notice before anyone asked you to fix it?"
- Precision questions:
  - "Did you create it, or work on something someone else designed?"
  - "Which tools did you use for that, and how: daily, built from scratch, or once?"
  - "Do you have a number for that (volume, time, people)? An estimate is fine if we label it as one."

**Block B — Hidden experience** (2–3 questions). Things outside formal jobs: side projects, volunteering, teaching, freelance work, tools they learned alone, processes they improved.

**Block C — Education, credentials and languages** (1–3 questions). Only what the CV leaves unclear: degree status (completed or in progress), licenses and where they are valid, language level for speaking and writing.

Do not ask about salary, schedule, location or job preferences here: that belongs to stage 2.

If the user contradicts the CV, ask which version is right.

## 4. Extract skills

From the facts and stories, draft the **Skills** section of EVIDENCE.md: concrete skills in the words job listings use ("contract review", "process mapping", "SQL"), each with the `E-` codes that prove it and a level (used once / regular use / built or taught it).

No soft skills like "communication" unless a fact shows them in action. Show the list to the user and ask: "Is anything missing, or anything you would not be comfortable defending in an interview?"

## 5. Close

- Make sure every fact has a short meaningful code (`E-ONBOARDING`, `E-AUDIT-TOOL`) and a **Limit** line where there is a risk of overclaiming.
- Only facts and limits in the file. No interview notes, no history, no comments.
- Show a short summary: roles covered, number of facts, skills, the main limits and what stays unconfirmed. Ask the user to read `profile/EVIDENCE.md` and correct anything; apply corrections by rewriting the fact in place.

Then suggest the next stage: `/routes`.
