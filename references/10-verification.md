# Phase 7 - Verify before you score

Before a role is scored or tailored, settle whether it still exists. This runs
first because a fit score on a dead requisition is wasted work, and a wrongly
declared dead requisition is a closed door the person never knows was open.

A real search this skill was built from produced five reproducible failures at
this step: a truncated board listing read as "nothing here", an unreachable API
drifting into a confident "gone", a visible closure statement thrown out for
the wrong reason, a guessed ATS token mistaken for a dead employer, and a live
role recommended without weighing how stale it was. This file exists so none of
those five happen the same way twice.

## Three verdicts, never two

Every checked role resolves to exactly one of:

- **LIVE** - found on the employer's own hiring infrastructure. Record the
  canonical URL and requisition id.
- **GONE** - the board was reachable, demonstrably served other current
  requisitions in the same session, and this one was absent.
- **UNVERIFIED** - no machine-readable source could be reached. Record what was
  tried and what failed.

State the rule plainly: **absence of evidence is UNVERIFIED, not GONE.** An
UNVERIFIED row is a known gap the person can act on - re-check later, ask them
to look themselves. A GONE row is a claim, and a wrong one closes a real
opportunity without anyone finding out. There is no default between the two;
where the evidence does not reach LIVE or GONE, the verdict is UNVERIFIED and
nothing else.

## Evidence is asymmetric - three tiers

This is the most load-bearing rule in this file.

- **Tier A - the employer's own ATS or careers board.** Settles LIVE and GONE.
- **Tier B - an explicit closure statement**, on any surface, including
  third-party boards: "no longer accepting applications", "this job is no
  longer available", or HTTP 404/410 on the employer's own domain. Settles
  GONE. **Never settles LIVE.**
- **Tier C - third-party existence and date claims**, e.g. "posted 2 days ago",
  "reposted yesterday". Settles nothing, in either direction.

The reasoning has to travel with the rule or the next maintainer who finds it
inconvenient will delete it: a hiring platform has no incentive to mark a live
requisition closed, and every incentive to keep a dead one listed - it is
inventory either way. So negative evidence from a weak source is strong, and
positive evidence from the same source is worthless. A rule that rejects both
is half wrong, and it was the version of this rule that shipped first. It
exists to stop stale third-party listings being read as live; it must not also
throw out a closure statement that is sitting on screen. See `04-sources.md`
for the existing rule that a third-party date field and a search hit are not
evidence of liveness - that rule stays. Tier B narrows it. It does not repeal
it.

## Prefer the single-record endpoint

When a requisition id is known, query the per-record endpoint for that id, not
the board listing. Board listings truncate without signalling it, and a row
missing from a truncated list is not an absent requisition - it is a list that
stopped rendering before it got there.

Where only a listing is available, treat any not-found result as UNVERIFIED
unless the response can be shown to be complete - an explicit total that
matches the number of records actually read. A listing that says "500 total"
and hands back 100 is not evidence the id in question does not exist; it is
evidence you read a fifth of the list.

## GONE requires a positive control

Never emit GONE from a failed lookup alone. In the same session, confirm the
board is serving other current requisitions - ideally fetch one known-good
record from the same board - and record which control was used. A 404 against
a board that is entirely down is not a dead requisition. It is an outage, and
an outage looks identical to a closure from the far end of a single failed
request.

## An empty board means a wrong token, not a dead employer

If a board endpoint returns zero records, the default explanation is an
incorrect board token, not an employer who has stopped hiring. Guessing a
token from the company name and treating the resulting empty board as "this
employer has nothing open" was a real failure mode, and it looked exactly like
a correct result. Resolve the real token before drawing any conclusion - the
employer's own careers page normally discloses it in an apply link or an
embed script.

A plain web search for the employer's name plus "careers" or "jobs" resolves
this faster than guessing variations. Search is for discovery here, not
verification - see the ladder below.

## Closure statements are trusted per source, not absolutely

One source was found to display a closure banner on every requisition it
carried, including ones the underlying ATS confirmed were open and accepting
applications. So Tier B is conditional: before trusting a closure statement
from a source not seen before, test it against a requisition known to be live
on that same source. If the source emits closure indiscriminately, record it
as an unreliable emitter and fall back to Tier A.

Keep that list of unreliable sources in the person's own working folder, not
in this repository - it is a fact about their search, not about the skill.

## The escalation ladder - cheapest first

Stop at the first tier that settles it, and log which one did.

1. **The employer's ATS single-record endpoint**, then the board with a
   control.
2. **The employer's own careers page or `sitemap.xml`** - often
   machine-readable even when the board itself renders client-side.
3. **A web search** to find the canonical URL, token or requisition id. Search
   is for discovery; the employer's board is for verification. A search result
   never establishes liveness. Note the known bias: general search tools are
   weighted toward some markets and will under-surface local domains, which is
   the wrong bias for a country-specific search - pair search with the
   employer's own domain rather than trusting the search alone.
4. **Ask the person to paste the listing card from their own logged-in
   session.** This is cheaper and faster than browser automation, it carries
   both the closure statement and the decay signals in one screenshot, and it
   respects the existing rule against scraping boards that forbid it - see
   `04-sources.md`. Ask before automating.
5. **Browser automation, last.**

## Record provenance per role

Every checked role stores: verdict, which tier settled it, the source, the
control used for a GONE, and the date. A verdict without provenance cannot be
re-audited, and this is exactly the kind of thing that does need re-auditing -
this file exists because a prior run's verdicts were wrong and nobody could
tell which ones without redoing the work from scratch.

## Generic endpoint patterns

The common ATS shapes, with `<token>` standing in for the employer-specific
piece. Confirm the real token before using any of these - see above.

- **Greenhouse** - single record:
  `boards-api.greenhouse.io/v1/boards/<token>/jobs/<job_id>` (GET). Listing:
  `boards-api.greenhouse.io/v1/boards/<token>/jobs?content=true` (GET).
- **Ashby** - listing (job detail is embedded in it):
  `api.ashbyhq.com/posting-api/job-board/<token>` (GET).
- **Lever** - single record:
  `api.lever.co/v0/postings/<token>/<posting_id>?mode=json` (GET). Listing:
  `api.lever.co/v0/postings/<token>?mode=json` (GET).
- **SmartRecruiters** - single record:
  `api.smartrecruiters.com/v1/companies/<token>/postings/<posting_id>` (GET).
  Listing: `api.smartrecruiters.com/v1/companies/<token>/postings` (GET).
- **Recruitee** - single record: `<token>.recruitee.com/api/offers/<offer_id>`
  (GET). Listing: `<token>.recruitee.com/api/offers` (GET).
- **Workable** - listing: `apply.workable.com/api/v1/widget/accounts/<token>`
  (GET), which carries each posting's own slug and URL.
- **BambooHR** - listing only, reliably: `<token>.bamboohr.com/careers/list`
  (GET). Treat any single-record claim on BambooHR as needing confirmation on
  the actual listing page before trusting it - the shape varies by account.
- **JazzHR** - board is server-rendered HTML rather than a JSON API in most
  deployments; treat the listing page itself as the source and confirm by
  reading it, not by assuming an endpoint.
- **Workday CXS** - single record:
  `<tenant>.<dc>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/job/<job-req-path>`
  (GET). Listing: `.../wday/cxs/<tenant>/<site>/jobs` - **POST only**, and
  cannot be reached with a GET-only tool. This is exactly the case the
  single-record-first rule above is for: the list endpoint being unreachable
  is not evidence about any requisition on it.
- **Eightfold** - implementation varies per employer; do not assume a fixed
  host. Look for the request shape in the employer's own careers page rather
  than guessing one - an invented endpoint that happens to return 404 reads
  exactly like a dead requisition and is the same error this file exists to
  stop.
- **Fallback for anything else** - the employer's own `/sitemap.xml` or
  `/careers/sitemap.xml`. Often lists individual job URLs even when the
  careers page itself renders client-side and nothing above reaches it.

Some list endpoints only accept POST and cannot be reached with a GET-only
tool. Where that happens, the single-record GET often still works even where
the list endpoint does not - use it, and do not read the list endpoint's
failure as anything about the employer.

Maintain a resolved-token registry in the person's working folder, so a token
resolved once is never re-hunted. Do not put resolved tokens in this
repository - see the anonymisation note in `README.md`; the working folder is
theirs, this repository is public.
