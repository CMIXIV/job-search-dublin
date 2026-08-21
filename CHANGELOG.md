# Changelog

Dates are release-tag dates. Each entry is a summary of the tagged commit;
see git history for the full message.

## v1.4.0 - 2026-08-21

Verification-correctness release. A live run against a real pipeline exposed
five reproducible ways phase 7 could get a role's liveness wrong: a truncated
board listing read as absence, an unreachable API drifting toward a guessed
"gone", a visible closure statement thrown out by a filter meant for
something else, a guessed ATS token mistaken for a dead employer, and a live
role recommended without weighing how stale it was.

Adds `references/10-verification.md` as a new phase-7 precondition: three
verdicts (LIVE, GONE, UNVERIFIED, never a guess between the last two), three
evidence tiers with the incentive-asymmetry reasoning attached, a rule that
GONE always needs a positive control, and an escalation ladder that puts
asking the person above browser automation. Adds decay signals to
`07-fit-scoring.md` that adjust Probability, explicitly never Fit. Adds two
hard rules to `SKILL.md` and four agent-discipline behaviours to
`behaviours.md` - reading a source before it ranks, one direction of data
flow, reading before overwriting shared artefacts, and owning a wrong call in
full. Adds `scripts/verify_check.py`, a regression check against recorded
fixtures that fails loudly if the verdict logic regresses.

## v1.3.1 - 2026-08-20

Lead the tracker with three named actions, not counts. A stats bar counts the
pipeline and decides nothing, and a sorted table still asks someone to
interpret thirty rows when they least want to. The tracker and the digest now
open with three named, dated actions instead, kept separate from the overdue
list, with a route-building action required whenever the week is cold-capped.

## v1.3.0 - 2026-08-20

Make source setup a precondition for scheduled discovery. A scan with no
configured sources silently degrades into repeated cold web searches and
reports the result as real, so the person concludes the market is empty when
the source stack is. Phase 6 now refuses to schedule until phase 4 is done and
names its coverage in every digest. Adds URL-shape classification for tracker
links, a rule that a filter without a number is not a filter, and a standing
behaviour of reporting what was not covered.

## v1.2.1 - 2026-08-18

Track agency routes and CV consent in the tracker. Hidden-employer listings
had no home in the schema, so there was nowhere to record which agency holds
a role or whether the person agreed to be submitted. Adds Via and Consent
columns, an explicit incident value for a CV sent without consent, and a
one-row-per-underlying-role rule. Xlsx formula column letters are now derived
from the header list rather than hard-coded.

## v1.2.0 - 2026-08-18

Add agency handling, fix the LinkedIn method, cap cold-route odds - from a
second round of real-search feedback. Agencies must not submit a CV before
naming the client. Plain LinkedIn keyword search under-returns badly and
postings churn within a day, so discovery moves off a weekly cadence.
Cold-only applications now cap Probability at 5. Adds hiring clusters,
repost-resets-the-clock, and a caution that inbound during a public layoff
spikes and decays. README corrected - it still advertised a single fit score
and three tracker tabs.

## v1.1.1 - 2026-08-18

Treat a job link as a fact, not a placeholder. A missing req URL was being
filled with something plausible - a search query, a board root, or the row
above's link - all clickable, all failing only when someone tries to apply.
Links now stay blank when unknown, with two validation checks: no two rows
share a URL, and every URL names its own company or req.

## v1.1.0 - 2026-08-18

Split fit from probability, add learned filters and chase ladder. Encodes
methodology from a live search: a single fit score conflated how well a role
matches with how likely it is to land, screening filters are learned from
declines rather than specified up front, and applications need a kill date.
Tracker gains Rejected-vs-Passed, a per-role honest-gap column, and interview
history.

## v1.0.0 - 2026-08-17

Initial release. Seven-phase redundancy job-search skill, plus an installable
`dist/` bundle and the release workflow that builds it.
