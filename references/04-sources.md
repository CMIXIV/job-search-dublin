# Phase 4 - Source stack

Goal: three or four sources that between them cover the target roles, set up with
alerts so discovery happens without the person having to remember to look.

Output: `job-search/04-sources.md` - what is configured, what each covers, and
what each misses.

## The distinction that matters

**Discovery** sources tell you a role exists. **Verification** sources give you
the real requisition, the full description and the working application form.

Aggregators are for discovery. The company's own board is for verification. A
role found on an aggregator should almost always be applied to on the company
board - the aggregator listing is often stale, truncated, or a duplicate posted
by an agency.

## Tier 1 - discovery, weekly, with alerts

**LinkedIn Jobs.** Broadest coverage, the only reliable source for
Principal-and-above and for roles that never reach aggregators. Set up saved
searches per target title with the synonyms from phase 2, turn on daily or weekly
alerts, and use "Easy Apply" filters sparingly - Easy Apply roles get hundreds of
applicants and convert poorly.

Do not scrape LinkedIn. Its terms forbid it, accounts get restricted, and the
alerts do the same job legally. Read pages the person already has open in their
own browser if you need to see a listing.

**Build the search URL properly - plain keyword search under-returns badly.** A
bare keyword search will hand back the same short, stale list run after run. The
same search with the filter parameters set - a real `geoId` for the city rather
than a typed location, an explicit `distance`, a date filter such as
`f_TPR=r86400` for the last 24 hours, and a salary floor where relevant -
routinely returns several times as many usable roles. Construct the URL once with
the person, save it, and re-run that.

This is using the site's own search with its own filters, in their browser. It is
not scraping and nothing here asks them to circumvent anything.

**The 24-hour window churns faster than a weekly scan.** Re-running the same
filtered search a couple of hours later surfaces roles the earlier pass did not
show. Postings appear, get promoted and get buried within a single day. A weekly
cadence will therefore lose roles silently - not because the search is wrong but
because the window moved. Tell the person this plainly and set the cadence
accordingly: see `06-cadence-autonomy.md`.

**A local tech job board.** In Dublin that is **Built In Dublin**; most tech
cities have an equivalent (Built In runs several, and there are strong local
boards elsewhere). These are frequently underrated: no login, visible posting
dates, work mode and seniority on the card, readable descriptions, and often an
AI summary per role. In the search this skill was built from, the local board
produced the majority of live applications.

Its weakness is the very top of the seniority band and non-local remote roles -
exactly the gap LinkedIn fills. Run both; they are complementary, not ranked.

**A cross-company ATS index.** `my.greenhouse.io` searches across every company
using Greenhouse in one place, and Greenhouse postings more often carry published
salary bands than anything else you will see. Smaller volume, high signal.

## Tier 2 - verification and per-employer monitoring

**Workday.** There is no cross-Workday search and there will not be one: every
employer runs an isolated tenant at `company.wd3.myworkdayjobs.com/SITE`, with no
shared index. Greenhouse can offer cross-company search because it hosts one
system; Workday deliberately does not.

The practical answer is per-employer email alerts. Pick the employers that matter
- for most people that is five to ten - and set a job alert on each tenant. Free,
reliable, and better than anything you could build for that number of companies.

**Ashby, Lever, Greenhouse boards, Personio, SmartRecruiters.** Same pattern:
find the target employer's board, apply there, set an alert if offered.

**A target-employer list is itself a source.** Twenty companies the person would
actually join, monitored directly, will out-perform passive browsing - especially
for roles that get filled before they are widely posted.

## Agencies and hidden-employer listings

A meaningful share of listings never name the employer - recruitment agencies
posting on behalf of a client, and aggregators that republish a role behind their
own branding. Treat them as a distinct source type, because they behave
differently from everything above.

**Log them, but log what you do not know.** The company field reads
`[EMPLOYER NOT DISCLOSED - via <agency>]`, never a guess. Two hidden listings can
easily be the same underlying role, and a guess makes that impossible to detect.

**Find the underlying posting before applying.** The role text is often
identifiable - paste a distinctive sentence into a search and the employer's own
posting frequently appears. Applying direct is better than applying through an
intermediary who takes a fee and controls the timeline.

**Never let an agency submit a CV before they name the client.** This is the rule
that protects the person, and in Ireland it has legal and code-of-practice force -
see `09-ireland-redundancy.md`. Blind submission risks the CV landing at their
current employer, at a company where they already have a live application, or at
one they have deliberately ruled out. It also creates duplicate-candidate
disputes that get the person dropped by both routes.

**Watch for the same role appearing three times.** One employer posting, one
agency version and one aggregator copy is common. The tracker should hold one row
with the routes noted, not three rows inflating the pipeline.

## Hiring clusters

Several roles appearing at one employer inside a short window - three in a day, a
handful in a week - is not three opportunities. It is a team being built, and it
means someone there has budget and a mandate right now.

Enter through **one conversation, not three applications**. Applying separately to
each puts the person in three parallel screens, often with the same recruiter, and
signals scattershot interest. A single message to the hiring manager or team lead
asking which of the roles best fits their background is a stronger opening and
frequently reaches a human faster.

Record the cluster in the tracker as a single entry with the roles listed, so it
does not read as three stalled applications a fortnight later.

## Tier 3 - the one that actually converts

**People.** Referred candidates convert at multiples of cold applicants, and a
redundancy is one of the few times it is socially easy to ask for help. This is a
source, so treat it like one: list former colleagues, managers and the people
inside target companies; record who was contacted and when in the tracker; follow
up. See `08-apply-and-followup.md` for the messages.

**Recruiters** are worth two or three good relationships, not twenty. Ask them
what they are actually seeing in the market - it is the fastest read on whether
the target band is realistic.

## Setup checklist

Walk through this with the person, one line at a time. Tick items in
`job-search/04-sources.md` as they are done.

1. LinkedIn: profile set to "Open to work" (recruiters-only if still employed),
   one saved search per target title, alerts on.
2. Local board: search each target title, note the live-posting count, subscribe
   to the alert.
3. `my.greenhouse.io`: account created, searches saved for each target title.
4. Target-employer list: 10-20 companies named, each board found, alert set.
5. Notice which sources need a login and get those created now, not at the moment
   a deadline is closing.

## Record the dead ends too

Negative findings save more time than positive ones, and they get re-derived
endlessly if nobody writes them down. Keep a short list in
`job-search/04-sources.md` of where *not* to look, with the reason and the date.

The pattern that catches most people: **a large office is not the same as a
function being decided there.** A company can employ thousands in a city and make
none of the decisions the person wants to be part of, because that function sits
at headquarters. The same holds for remote roles - plenty of companies hire
engineers across a continent while keeping product, design or leadership in one
time zone. Check whether the *function* is hired there, not whether the company
is present.

Other dead ends worth recording: sources that return nothing at the target
seniority, employers who never reply, and search lanes (a location, a work mode,
a title) that produced zero live roles across several weeks. A lane that is
structurally empty is a finding, not a run of bad luck - say which one it is.

## Practical gotchas

- **LinkedIn job descriptions are gated.** Search result lists read fine; the
  descriptions frequently do not. Pull the JD from the company's own board.
- **Cross-company ATS search needs its filters set exactly.** On
  `my.greenhouse.io` the location filter only works with the full parameter set -
  query, location, latitude, longitude, location type and country. Passing the
  country alone is silently ignored and returns global results, which looks like
  a working search full of the wrong roles. Check the first few hits are actually
  in the target location before trusting a result set.
- **Signed-in sources persist.** Sources needing a login are worth the one-time
  setup; the session usually lasts, and they surface roles that appear nowhere
  else.

## Record what each source is producing

Every role that enters the tracker records the source it came from. After three
or four weeks, count roles found and applications submitted per source, and
reweight the time spent.

Do this from the data, not from impression. Impressions about sources are
unreliable in both directions - it is entirely possible to talk yourself into
dropping the source that is producing most of your pipeline.
