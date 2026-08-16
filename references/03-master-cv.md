# Phase 3 - Master CV, and tailoring from it

Two documents, not one.

**The master CV** is the source of truth: everything provable, in the person's
own framing, maintained once. It is never sent anywhere.

**The tailored CV** is what gets sent: the master, cut and reordered against one
specific job description. Produced in minutes because the master already exists.

Explain this split up front. People resist maintaining two things until they see
the fifth tailored CV take four minutes instead of an evening.

## Build the master

Source of truth is `job-search/03-master-cv.md` - plain markdown, easy to edit,
diffable. Generate `.docx` and `.pdf` from it. Start from
`templates/master-cv-template.md`.

**Structure that works for experienced hires:**

- **Header** - name, title line, location, phone, email, LinkedIn. Nothing else.
- **Profile** - three or four lines. The distinctive combination from phase 1,
  with the two biggest numbers in it. Not a mission statement.
- **Skills** - grouped, scannable, honest. Includes the exact keywords the target
  roles use, because a human recruiter greps this section in six seconds.
- **Experience** - reverse chronological, most recent role longest.
- **Education, certifications, publications** - short, at the end.

**Two pages, and be deliberate about where the fold falls.** Page 1 should cover
the recent years that match the target. Compress everything older into short
blocks on page 2. A recruiter who reads only page 1 should see only the relevant
story - that is the point of the ordering, and it is worth stating to the person
so they do not read the compression as erasure of their early career.

**Merge repeated employers.** Three roles at the same company become one entry
with the titles listed inline. It saves eight lines and reads as tenure rather
than churn.

**Every bullet is outcome-first.** Verb, what changed, by how much, over what
scope. "Owned fraud detection for a payments platform processing EUR 4bn a year
across 14 markets, cutting false positives by 40%" beats "Responsible for fraud
prevention" - and it is the same fact.

**Placeholders stay visible.** Anything unknown goes in as `[ADD PHONE NUMBER]`,
`[NEEDS NUMBER]`, `[CONFIRM DEGREE]` - in the document, in capitals, impossible
to miss. List them again in your reply. Never fill one in with a plausible guess.

## ATS rules - not optional

Most applications are parsed by software before a human sees them. The failure
mode is silent: a beautiful CV that arrives as scrambled text.

- One column. No tables, no text boxes, no sidebars, no columns.
- Nothing important in headers or footers - many parsers drop them entirely.
- Standard section names: Experience, Education, Skills. Not "My Journey".
- Standard fonts, real bullet characters, no icons for contact details.
- Dates in a consistent format, month and year.
- Send `.docx` when the form allows it, `.pdf` when it does not care. Never send
  an image, a Pages file, or a link when a file is asked for.
- File name: `Firstname-Lastname-CV.pdf`. Not `CV_final_v3_updated.pdf`.

**Verify by round trip.** Render the document, extract the text back out with
`scripts/ats_check.py`, and confirm every key claim, every number and every
section heading survived. If a claim does not survive extraction, an ATS will not
see it. Show the person the result - it is the difference between "I made you a
CV" and "I made you a CV and proved a machine can read it".

## Check the CV against LinkedIn

Recruiters cross-reference. Any place the two disagree on scope, dates or title
is a credibility risk, and the CV is usually the one that got updated.

List every discrepancy, say which version you believe and why, and tell them
which side to fix. Then remember: LinkedIn edits are theirs to make, not yours.

## Tailoring per role

Do this only after the role scores well enough to be worth the time (phase 7).

1. Extract from the JD: required skills, preferred skills, the seniority signals,
   the domain language, and the three things the ad repeats - repetition is what
   the hiring manager actually cares about.
2. Reorder, do not rewrite. Move the matching experience up. Promote the matching
   bullets within each role. Cut the bullets that do not serve this application.
3. Mirror their vocabulary where it is honest. If they say "experimentation" and
   the master says "A/B testing", use theirs. If they say "Kubernetes" and the
   person has never touched it, that stays out - keyword-stuffing gets caught at
   interview and costs more than the screen was worth.
4. Rewrite the profile paragraph for this role. Four lines, their language, the
   two most relevant numbers.
5. Keep it to two pages. Something must come out for anything that goes in.
6. Re-run the ATS check on the tailored version.
7. Save to `job-search/applications/<company>-<role>/` alongside the JD snapshot
   and the fit score, so the interview prep three weeks later has the exact
   document that was sent.

**Never add a claim during tailoring that is not in the master.** If tailoring
tempts you to invent something, the honest move is to note the gap and let the
person decide whether to address it in the cover note.
