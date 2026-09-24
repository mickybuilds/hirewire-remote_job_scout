# CV format and writing rules

Harvard format, readable by ATS filters. Facts come only from `profile/EVIDENCE.md`.

## Format

Markdown for `scripts/make_docx.py`, which produces the final layout (Times New Roman, one column, real bullets, right-aligned places and dates).

```
# FULL NAME
City, Country (remote, UTC±X) | phone | email | LinkedIn URL

## Experience
### Organization || City, Country
_Role title_ || Mon YYYY – Mon YYYY
- Bullet.

## Education
### Institution || City, Country
_Degree_ || YYYY

## Additional
### Project or credential || YYYY
- Bullet.

## Skills & Languages
**Skills:** skill, skill, skill
**Languages:** Language (level), Language (level)
```

- Section order: Experience, Education, Additional (only if it adds something for this listing), Skills & Languages. Education goes first only when the candidate has less than two years of relevant experience.
- No summary or objective by default. Add a 1–2 line **Profile** section after the contact line only when the candidate is changing fields and the link to the role is not obvious from the experience.
- Section names in the CV language. Spanish: Experiencia, Educación, Información adicional, Habilidades e idiomas.
- Dates in the CV language (Spanish: "mar. 2020 – actualidad").
- 3–5 bullets per recent role, 1–2 per older role. One page for less than 10 years of experience, two at most.
- No tables, columns, icons, photos, graphics, skill bars, headers or footers. Contact data goes in the body.

## Writing

Each bullet: **verb + what + context + result or deliverable**, one or two lines.
- Start with a concrete verb, first person without the pronoun: past tense for finished work, present for ongoing work in the current role. English: built, reviewed, trained / build, review. Spanish: creé, revisé, capacité / escribo, gestiono. Never third person ("creó", "gestiona").
- Plain, specific words. Say what was done, for whom and what came of it.
- Numbers only when EVIDENCE.md has them. An estimate stays labeled as an estimate ("about 5 cases per week").
- Participation is written as participation: "contributed to", "took part in". Never turn it into leadership or authorship.
- Use the listing's terms only when they describe something the candidate actually did.
- Skills: 6–10 concrete skills or tools that the listing asks for and the evidence supports. No soft skills in this list.

Never use, in any language:
- empty adjectives and self-praise: passionate, dynamic, results-driven, highly motivated, detail-oriented, hard-working, team player, proactive, go-getter, apasionada, dinámica, proactiva, orientada a resultados, altamente motivada, detallista;
- inflated or vague phrases: proven track record, extensive experience, strong background, expert in, world-class, cutting-edge, amplia experiencia, sólidos conocimientos, vasta trayectoria, de vanguardia;
- corporate filler: leveraged, spearheaded, synergy, drove impact, fostered, orchestrated, empowered, seamless, robust, dynamic environment, fast-paced, potencié, lideré (unless there was formal leadership), sinergia, entorno dinámico;
- decoration typical of generated text: em dashes inside sentences, triple lists of adjectives, rhetorical closings, bold words in the middle of bullets, emojis.

## Final check

Before generating the file, reread every line and ask:
1. Which `E-` code backs it? If none, delete it.
2. Does it break a **Limit** of that code? If so, rewrite it.
3. Does it contain a word from the list above? If so, replace it with the concrete fact.
4. Would the candidate be comfortable explaining it in an interview? If not, soften it to what they did.
