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
- **A generated HTML dashboard** - a single self-contained file with the data
  inline, filters, sortable columns and an overdue view. Excellent to *read* and
  review from, poor for data entry. Works best regenerated from the spreadsheet
  rather than replacing it.
- **A dedicated job-search app** (Teal, Huntr and similar) - browser extensions
  that capture roles in one click, which is genuinely useful. The cost is that
  the data sits in someone else's product and is harder for you to work with.
  Fine if they prefer it - then keep the tracker as the summary layer.

Generate the file with `scripts/make_tracker.py`. It writes an `.xlsx` and a
`.csv`; the CSV imports into Sheets, Notion and Airtable cleanly.

Record the location in `job-search/00-state.md`.

## Schema

Four tabs. Resist a fifth - every extra column is a thing that quietly
stops being filled in. The narrative columns (Why, Watch, Route, Next) are the
exception worth defending: they are where the thinking lives, and a tracker
without them degrades into a list of links within a fortnight.

**Applications** - one row per role:

| Field | Why it earns its column |
|---|---|
| Rank | Sort by Priority. The top of this column is the answer to "what now" |
| Date found | Age of a posting predicts response rate |
| **Source** | The attribution that tells you where to spend time |
| Company / Role | `[EMPLOYER NOT DISCLOSED]` where a listing hides it. Never guess |
| Via | The agency or intermediary holding the role. Blank means direct |
| Consent | Whether they have agreed to be submitted, and to whom. See below |
| Band | Senior / Lead / Principal / Director - reveals where they actually land |
| Depth | High / Medium / Low - is their differentiator the core of the role |
| Location / mode | Onsite, hybrid days, remote-within-country. Record contradictions here as a question to ask |
| JD link | The req URL on the company's own board. Blank if you do not have it - see below |
| Posted | Req ID and posting age - stalled, shortlisted, or hard to fill |
| Salary band | Published band if there is one; blank is data too |
| **Fit** | 1-10, maps to what they have shipped |
| **Probability** | 1-10, honest odds of landing it |
| **Priority** | The two weighted equally, adjusted for comp and title |
| Why | What makes this worth pursuing, including anything learned from inside |
| **Watch** | The one thing that could sink it, named honestly |
| Route | How this application gets in - direct, referral, advocate, recruiter |
| Advocate | Who inside, and the relationship. The strongest single predictor, and the one worth creating |
| Status | See the vocabulary below |
| Date applied | Starts the chase clock |
| Next / Due | The literal next action and its date. Sorting by Due is the week's to-do list |
| CV used | Path to the exact file sent |
| Notes | Interviewers, questions asked, salary discussed |

**Status vocabulary.** Keep these distinct - the distinctions are what make the
tracker analysable:

`Alert only` (monitoring, not pursuing) · `Not started` · `Researching` ·
`Applied` · `Recruiter call` · `In process` · `Onsite/Final` · `Offer` ·
`Rejected` (they declined you) · `Passed` (you declined them, or you closed a
dead application at day 30)

**Rejected and Passed are not the same status.** Rejected measures the market.
Passed measures the person's own filters - and reviewing the Passed rows with
their reasons is exactly how the screening filters in `07-fit-scoring.md` get
discovered. A tracker that cannot express "I decided against this, because" loses
the more useful half of the data.

**Interview history** gets its own tab. Keep a permanent list of every company and level where a
process ended, with any feedback given. It stops low-value re-applications and
turns an old rejection into a prepared answer instead of a surprise.

**Contacts** - one row per person: name, company, relationship, how they can
help, last contact, next follow-up, notes. Referrals convert far better than cold
applications, so this tab deserves the same discipline as the first.

**Interview history** - company, role, level, date, stage reached, outcome, any
feedback given. Permanent; it outlives the current search.

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

**Track where every copy of the CV has gone.** Once agencies are involved, the
person loses sight of who holds their CV and who it has been shown to - which is
the thing that causes duplicate-submission rejections and the CV arriving back at
their own employer. The `Via` and `Consent` columns exist to make that visible at
a glance:

`Direct - n/a` · `Asked, awaiting client name` · `Consent given` ·
`Consent withheld` · `SUBMITTED WITHOUT CONSENT`

The last value is an incident record, not a status. It is shouty on purpose: it
means a CV went somewhere the person did not agree to, and it is the evidence if
a complaint follows. See `09-ireland-redundancy.md` for what to do about it.

**One row per underlying role, not per route.** The same job routinely appears
three times - the employer's own posting, an agency version with the employer
hidden, and an aggregator copy. Three rows inflate the pipeline and hide the fact
that two applications are competing for one seat. Merge them into one row, note
the routes, and if a hidden listing later turns out to be a role already tracked,
merge rather than delete so the duplication stays visible.

**A link is a fact. Capture it or leave it blank.** The JD link must be the URL of
*that specific requisition*, captured at the moment of scoring. If you do not have
it, the field stays empty or reads `[NO LINK CAPTURED]`.

Three things that are not links, however much they look like one:

- a search query - `linkedin.com/jobs/search?keywords=...`, `my.greenhouse.io/jobs?query=...`
- a careers-site or board root - `jobs.ashbyhq.com/company`, `company.com/careers`
- the URL from the row above, pasted because this row had none

The third is the dangerous one. All three fail silently: they are clickable, they
look right in the table, and they only reveal themselves when someone opens the
row to apply and lands somewhere else. Substituting a plausible URL for a missing
one is the same error as inventing a metric for a CV - except that nobody thinks
of a link as a claim.

**Two checks that catch it.** Run them whenever rows are added in bulk:

1. **No two rows share a link.** A duplicate means one was copied from its
   neighbour.
2. **Every link contains a token from its own row** - the company name, or the req
   ID. A link naming a different company than the row it sits on is wrong by
   definition.

Postings expire, so save the JD text alongside the link at capture time. A dead
URL with the description saved is recoverable; a dead URL alone is not.

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
- Warm versus cold conversion - referral and advocate routes against cold
  applications. When the gap is large, reallocate the week accordingly
- The Passed rows and their reasons - the raw material for new screening filters
- Band distribution across applications versus responses. If applications one
  band up get nothing and applications at band get screens, the market has
  answered the phase 2 title debate
