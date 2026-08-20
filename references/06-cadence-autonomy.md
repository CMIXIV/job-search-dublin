# Phase 6 - Cadence and autonomy

Two settings: how often the search runs, and how much of it happens without the
person in the loop. Ask for both explicitly and record them in
`job-search/00-state.md`.

## Cadence

Derive it from the runway in phase 2, and state the trade-off rather than
prescribing.

- **Short runway (under 4 months)** - discovery twice a week, 8-12 applications a
  week, network outreach every week. Volume matters more than perfect tailoring at
  this end; a good tailored CV in 20 minutes beats a perfect one in two hours.
- **Medium (4-9 months)** - weekly discovery, 4-6 applications, deeper tailoring,
  more time on target employers and referrals.
- **Long, or currently employed** - fortnightly discovery, 2-3 high-fit
  applications, most of the effort in relationships and positioning.

Pick a fixed slot in the week and name it. "Monday morning" beats "weekly".

**One caveat that overrides the above: discovery cannot be weekly.** Job postings
churn inside a single day - the same filtered search run two hours apart returns
roles the first pass did not show. A weekly scan does not find fewer roles because
the search is bad; it finds fewer because most of them appeared and got buried
between scans, and nothing tells you they existed.

So separate the two rhythms. **Discovery runs daily or every other day** and takes
five minutes - open the saved filtered search, skim, log anything worth scoring.
**The deeper work - scoring, tailoring, applying - keeps the weekly slot.** If the
person can only manage one rhythm, make discovery the automated one, since it is
the part that decays without attention.

**Warn about the volume trap.** Response rates for cold applications are low
everywhere, so people rationally increase volume - and volume degrades tailoring,
which lowers the response rate further. The escape is not more applications; it
is more applications *with an advocate*. If the weekly count is being hit and
nothing is converting, the fix is in `08-apply-and-followup.md`, not in the
number.

## Autonomy levels

Three levels. Default to L1. Higher levels are opt-in, and the person should be
told exactly what they are taking on.

### L0 - Manual

Nothing happens unless the person starts a session. You are a co-pilot: they
bring roles, you score, tailor, and draft.

Choose this if they want to stay close to every step, or if they are not ready to
have job alerts arriving while they are still processing the redundancy. That is
a legitimate reason and it should be offered without judgement.

### L1 - Scheduled discovery, manual application (default)

A scheduled task runs on the chosen cadence and produces a digest: new roles from
each source, each scored, sorted, with a recommended action. Nothing is sent.
The person reads the digest and decides what to pursue.

What can go wrong: a digest arrives during a bad week and lands as pressure. Say
this up front and make it easy to pause - a paused search is a decision, not a
failure.

### L2 - Scheduled discovery plus prepared applications

Everything in L1, plus: for roles above an agreed fit threshold, the tailored CV
and cover note are drafted and staged in
`job-search/applications/<company>-<role>/`, ready for review. Application forms
can be pre-filled in the person's own browser.

**A human still presses submit. Always.**

What can go wrong: staged drafts create a sense of obligation, and quality drops
if drafts get sent without being read. The rule is that every draft gets read
before it goes - if that stops happening, drop back to L1.

### Why there is no L3

Unattended auto-submission is deliberately not built, for four reasons worth
stating plainly:

1. **It cannot be undone.** A bad application to a target employer burns that
   employer, sometimes permanently. There is no rollback.
2. **The failure is invisible and correlated.** A misconfigured filter does not
   send one bad application, it sends forty, and nobody notices for a week.
3. **It requires scraping or automating sites whose terms forbid it.** The
   account restricted is the person's own, mid-search.
4. **The bottleneck is not submission.** People do not fail to get hired because
   they cannot press submit. They fail on fit, on tailoring, and on the absence
   of an advocate. Automating submission optimises the one step that was never
   the constraint.

If someone wants it anyway, be straight: it is their account, their reputation
and their market. This skill will help them apply faster and better; it will not
press send for them.

## Phase 4 is a precondition, not a suggestion

**Do not schedule discovery until the sources from `04-sources.md` are actually
configured.** This is the failure mode that quietly wrecks the whole loop, and it
is invisible from the outside.

If there is no saved LinkedIn search, no board alert and no per-employer alerts,
then a scheduled "scan" has nothing to scan. What it does instead is run the same
cold web searches every time - which returns the same aggregator noise week after
week, misses everything that requires a login or a filter, and produces a digest
that looks like a real scan and is not one. The person then reasonably concludes
the market is empty, when what is empty is the source stack.

So before scheduling anything, check and say out loud:

- Which sources are configured, by name
- Which are not, and what setting each one up would take
- What the scan will therefore actually cover

If nothing is configured, **say that plainly and fix it first**. A digest built
on cold search is worse than no digest, because it manufactures false confidence
that the ground has been covered.

Re-check this whenever results go quiet. "The market has gone quiet" and "my
sources stopped working" produce identical-looking weeks, and only one of them is
about the market.

## Setting up the schedule

Create a scheduled task at the chosen cadence that runs discovery, scores new
roles, updates the tracker, and delivers the digest. Include in it:

- **The three things to do next, named as actions, in order** - the first thing
  in the digest, before any counts or lists. See `05-tracker.md`
- **Which sources were actually run**, named, and which were not
- **How deeply each was covered** - roles read in full versus seen at headline
  level only. "Ten postings seen on the board, none opened" is a materially
  different result from "ten read and scored", and reporting them the same way
  turns an unfinished scan into a false all-clear
- New roles per source, with Fit, Probability and one-line rationales
- **What was found and deliberately not added, with the reason** - wrong function,
  wrong level, language requirement, failed a standing filter. This is how the
  person audits the filters instead of trusting them blindly, and it is where the
  next standing filter usually comes from
- Applications with a next action due this week
- Applications with no response past the follow-up threshold
- One honest line on how the week went against the target

**Deduplicate against the tracker, not against the last digest.** Scheduled tasks
sometimes fire twice in a day, and a second pass will happily re-surface roles
already logged. Match new finds against what is already in the tracker before
reporting them, or the pipeline inflates with duplicates of itself.

Make pausing trivial and say so when setting it up.

## Reviewing the settings

Revisit monthly, or immediately if runway changes, an offer arrives, or the
person says the digests are not being read. Digests going unread is data - it
usually means the cadence is wrong or the scores are not trusted, and both are
worth naming directly.
