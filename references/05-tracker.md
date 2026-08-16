# Phase 5 - Tracker

Goal: one place that holds every role, every application and every next action -
chosen by the person, not by you, because a tracker they will not open is worse
than no tracker.

## Ask, then set it up

Ask where they want it. Give the honest trade-offs and a recommendation, then
build whatever they pick.

- **Google Sheets** - works on their phone, survives after they stop using this
  agent, easy to share with a partner or a career coach. Needs a Google account
  and, for you to update it directly, a connector. The usual best answer.
- **Local spreadsheet** (`.xlsx`) - no accounts, fully private, works offline. No
  phone access, and version drift if they email it around.
- **Notion or Airtable** - nicer views, richer fields, good if they already live
  there. Setup cost and an authorisation step; a bad choice if they are adopting
  the tool solely for this.
- **A dedicated job-search app** (Teal, Huntr and similar) - browser extensions
  that capture roles in one click, which is genuinely useful. The cost is that
  the data sits in someone else's product and is harder for you to work with.
  Fine if they prefer it - then keep the tracker as the summary layer.

Generate the file with `scripts/make_tracker.py`. It writes an `.xlsx` and a
`.csv`; the CSV imports into Sheets, Notion and Airtable cleanly.

Record the location in `job-search/00-state.md`.

## Schema

Three tabs. Resist adding a fourth - every extra column is a thing that quietly
stops being filled in.

**Applications** - one row per role:

| Field | Why it earns its column |
|---|---|
| ID | Stable reference for conversations |
| Date found | Age of a posting predicts response rate |
| **Source** | The attribution that tells you where to spend time |
| Company | |
| Role title | |
| Band | Senior / Lead / Principal / Director - reveals where they actually land |
| Location / mode | Onsite, hybrid days, remote-within-country |
| JD link | The company-board link, not the aggregator link |
| Salary band | Published band if there is one; blank is data too |
| Fit score | 1-10 from `07-fit-scoring.md` |
| Score note | One line. Why that number |
| Status | Found, Shortlisted, Applied, Screen, Interview, Final, Offer, Rejected, Withdrawn, No response |
| Date applied | Drives the follow-up clock |
| CV used | Path to the exact file sent |
| Advocate | Internal contact and relationship - the strongest single predictor |
| Next action | The literal next thing to do |
| Due | Date. Sorting by this column is the weekly to-do list |
| Last contact | |
| Notes | Interviewers, questions asked, salary discussed |

**Contacts** - one row per person: name, company, relationship, how they can
help, last contact, next follow-up, notes. Referrals convert far better than cold
applications, so this tab deserves the same discipline as the first.

**Source summary** - roles found, applications submitted, screens, interviews,
per source. Formulas do this automatically in the generated file. Read it monthly
and reweight where the time goes.

## Rules for keeping it honest

**One row per role, added the moment it is found**, before deciding whether to
apply. A tracker that only contains applications cannot tell you what you passed
on, or why.

**Status changes get a date.** "No response" after 21 days is a status, not a
gap - it is how the market's response rate gets measured.

**Every row has a next action and a due date, or it is closed.** Rows with
neither are where searches go quiet.

**Never let the tracker become the work.** Five minutes a week of maintenance. If
it is taking longer, columns are being tracked that no decision depends on.

## What to read out of it

Monthly, compute and say out loud:

- Applications per week against the target set in phase 2
- Response rate overall, and by source
- Response rate by band - if Principal applications get nothing and Lead
  applications get screens, that is the market answering the phase 2 debate
- Advocate effect - response rate with an internal advocate versus without
- Where roles are dying: no response, screen, or final round. Each failure point
  has a different fix, and guessing which one is happening wastes weeks
