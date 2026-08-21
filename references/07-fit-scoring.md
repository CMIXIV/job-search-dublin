# Phase 7a - Screening, scoring and priority

Three numbers per role, not one, and a set of filters that gets applied before
any of them. The point is not precision. It is a consistent basis for deciding
where a limited number of tailoring hours go, and a record that stops the same
argument being had twice.

## Screen first - before scoring, before tailoring

**Verify before anything else.** Run `references/10-verification.md` first.
LIVE roles get scored. GONE roles do not - there is nothing to score. An
UNVERIFIED role can be scored provisionally, marked as such in the row, and
re-checked; treating UNVERIFIED as GONE and dropping it silently loses roles
that were never actually confirmed dead.

**Hard gates.** If a role fails one of these it is out, whatever it looks like.
Name the gate and move on.

- **Work authorisation** - can they legally be employed there, without
  sponsorship the employer will not provide
- **Location** - "remote" often means remote-within-one-country for tax reasons.
  Check the practicals before spending an hour on the application
- **Compensation floor** - if a published band sits below the phase 2 floor, out.
  No published band is not a gate; it is a question for the first call
- **Deal-breakers** from phase 2 - industry, travel, on-call, management scope

**Learned filters.** These are the ones that matter, and they do not exist at the
start. Every time the person declines a role, ask whether the *reason* should
become a standing filter. After a few declines a real screen emerges - and each
filter then saves an entire tailoring cycle every time it fires.

Filters that have come out of real searches:

- **Core-domain depth** - is the person's differentiator the *core* of the role,
  or bolted onto general craft? (See the depth test below.)
- **Builder, not advisor** - does the role involve building and shipping, or
  advising people who do? Advisory roles can pay well and carry a title, and
  they are a hard path back.
- **Culture** - screen before tailoring effort goes in, not after. Someone
  leaving a redundancy trades employment protection for a probation period, so a
  demanding culture is a worse bet from that position than from a stable job.
- **Compensation** - a floor stated once and applied without renegotiating it
  role by role.

Write each filter down with the decline that produced it. A filter with a story
attached gets applied; an abstract preference does not.

**A filter without a number is not a filter.** "Contract is fine if the rate is
right", "I'd relocate for enough money", "senior is acceptable at a good company"
all sound like decisions and none of them are. Every instance gets re-argued from
scratch, which is precisely what the filter was supposed to prevent.

Push for the figure at the moment the filter is created, while the example that
prompted it is in front of them - the day rate floor, the salary that justifies
the move, the conditions that make a lateral title acceptable. If they genuinely
cannot answer yet, record that as an open item with a date, not as a filter.

For contract and day-rate roles specifically: the rate is a first-call question
and never goes in an application. But the floor is agreed in advance, privately,
so the first call is a check rather than a negotiation with themselves.

## Three numbers

**Fit /10 - does this map to what they have actually shipped?**

Score against their evidence, not their aspirations. Take the three things the
job description repeats - repetition is the tell for what the hiring manager
cares about, more reliable than the order of the bullet list. Three of three with
concrete evidence is a 10. One of three is a 3.

**Probability /10 - honest odds of landing it.**

A different question, and the one people skip. Account for: the hiring bar, title
stretch relative to evidenced scope, domain distance, applicant pool, posting
age, whether an internal advocate exists, and process speed against the person's
deadline. A brilliant fit at a company that runs six-week loops is worth less to
someone with eight weeks of runway than a good fit that moves in ten days.

**Priority - what to actually do first.**

Fit and Probability weighted equally is the right default. Then adjust for comp
fit and title, and say what the adjustment was: *"scores 7.5, sits at 8 because
the comp band clears the floor."* Sort the tracker by Priority. That ordered
list is the answer to "what do I do next", which is the only question the
tracker exists to answer.

Keeping the two scores separate is the whole point. A 10-fit role with odds of 3
ranks below a 7-fit with odds of 8, and a single blended score cannot say that.

**Cold-only applications cap Probability at 5.** No route in - no advocate, no
referral, no prior contact, no reply from anyone - means the application competes
purely on paper against every other applicant, and the observed conversion is
poor. Real searches produce the same shape repeatedly: a stack of cold
applications returning nothing or a two-day CV-screen rejection, alongside a
single warm introduction reaching a hiring-manager conversation inside 48 hours.

So the cap is not pessimism, it is calibration. Applying that ceiling has two
useful effects. Cold roles stop crowding the top of the list on Fit alone, and
the way to raise a role's Priority becomes obvious - **find a route in**, which is
the action that actually moves the odds. Lift the cap the moment a route exists
and record what changed.

Where a whole week's list is cold-capped, that is the finding, not the roles. See
`08-apply-and-followup.md`.

## Decay signals - live is not the same question as winnable

Liveness (`references/10-verification.md`) answers *does this requisition
exist*. It gates whether a role is scored at all - an UNVERIFIED or GONE role
does not reach this section. Decay answers a different question: *is this
worth an application, given how it has aged*. It adjusts Probability only.

**Decay never changes Fit.** Fit measures the match between the person and the
role, and a requisition being old does not make it a worse match. Moving Fit
to justify a recommendation - or a decline - is the exact self-deception
"Never distort a score to express a preference" above already prohibits. A
stale posting is a Probability problem, not a Fit problem, and scoring it as
one hides the reason from the next person who reads the row.

Signals to weigh, each with what it actually means:

- **A repost flag at all.** The first attempt to fill it failed, or it is a
  standing pipeline requisition. Either way, the bar or the process is not
  what a fresh posting implies.
- **Age since posting or reposting.** Use explicit bands rather than
  judgement call each time: **under 3 weeks** - no adjustment. **Beyond
  roughly 6 weeks** - a visible cut. **Beyond roughly 3 months** - a heavy
  cut, stated in the row.
- **An evergreen or pipeline requisition id** - not a specific opening but a
  standing "always be sourcing" listing. Treat as a heavy cut regardless of
  fit, and say so in the row.
- **Applicant counts in the hundreds.** A crowded field competing on paper
  alone. Cut.
- **"Promoted" or sponsored.** Genuinely ambiguous - either urgency or
  difficulty filling. Note it in the row; do not score it alone.
- **"Responses managed off-platform."** Not a decay signal - a routing hint.
  It names where the real ATS is, which shortens the next verification. See
  the escalation ladder in `references/10-verification.md`.

Write the adjustment into the role's notes with its reason, the same
discipline as the comp-and-title adjustment under Priority above. A cut
without a reason cannot be argued with, and a person who disagrees with a
silent cut will just distrust the whole score instead of the one signal that
drove it.

## The depth test

Is the person's strongest differentiator the *core* of this role, or a feature
attached to it? A role whose centre is the thing they are best at will interview
on their strengths. A role with that thing bolted on will interview on general
craft, where they compete with everyone.

Score it High, Medium or Low and make it a sort key alongside Priority. It is
usually the fastest way to see that a pipeline full of 7s contains no roles the
person would actually be excellent at.

If the High-depth list runs dry without an offer, that is a decision point, not a
reason to drift - see `02-priorities.md`.

## Never distort a score to express a preference

When a role is declined for a reason that is not fit, do **not** quietly lower
its Fit score to justify the decision. The score becomes fiction and every
comparison after it is corrupted.

Add a dimension instead. A preference that keeps recurring is a filter or a
column, not a thumb on an existing scale. This is the single most useful scoring
discipline to hold, and the easiest to break.

## What the numbers mean

- **Priority 9-10** - drop other work, apply this week, activate every advocate
- **7-8** - apply with full tailoring, worth two hours
- **5-6** - apply if weekly capacity is not full. Prioritise those with an
  advocate or an unusually strong single dimension
- **3-4** - skip unless there is an advocate or a specific reason. Log the
  decline and its reason so it is not re-litigated
- **1-2** - no

## Score twice, and be willing to go down

**Pass 1** on the listing card - title, company, band, location, summary. Cheap,
fast, filters the list.

**Pass 2** after reading the full job description on the company's own board.
Scores move here, and they move down at least as often as up. A role that reads
as an AI product role in the summary can turn out to be mostly compliance work
once the responsibilities are listed.

State the revision explicitly: *"Reading the full JD lowered this from 8 to 7 -
the AI content is implied rather than stated, and the compliance domain is new."*
A score that only ever moves up is not a score.

## Read the posting, not just the requirements

- **Posting age** is evidence to interpret, not just a competition signal. A role
  live for 30+ days is stalled, has a shortlist, or is genuinely hard to fill -
  and the third case favours an unusual candidate. Say which one you think it is.
- **Contradictions inside the JD** - the structured field says hybrid, the body
  text says flexible - get recorded as a question to ask, not resolved by
  assumption. Put it in the tracker where it will be seen before the first call.
- **Several near-identical reqs at one employer** means reqs are being opened and
  closed quickly. Check whether the others are still open before assuming one
  rejection closed the door.
- **Several *different* roles at one employer in a short window** is a hiring
  cluster - a team being built by someone with budget right now. Score it as one
  opportunity entered through a single conversation, not three applications. See
  `04-sources.md`.
- **Published salary bands** are rare outside a few ATS platforms. Where no band
  is published, any figure is a hypothesis to test on the first call, not data.

## Record it

Tracker fields: Fit, Probability, Priority, depth, and one line of rationale for
each number. When a score changes, record the revision and the reason.

Save the JD text to `job-search/applications/<company>-<role>/jd.md` at the time
of scoring. Postings disappear, and interview prep needs the original.

**Capture the req URL in the same moment, or record no URL at all.** Scoring is
the only point at which you reliably have the specific posting open. A search
query, a board root, or the previous row's URL are not links - they are guesses
wearing a link's clothing, and they fail silently at the worst possible moment.
Before handing over any batch of scored roles, check that no two share a URL and
that each URL names its own company or req. See `05-tracker.md`.
