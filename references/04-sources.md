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
alerts do the same job legally.

**Reading a person's own saved search through their logged-in browser** -
including paging through it and opening individual listings - is not
scraping, provided it stays inside their authenticated session at ordinary
browsing pace: no raw requests to LinkedIn's endpoints, no bypassing login or
bot-detection, no extracting at a scale beyond what the person would see
themselves paging through the same search. Claude in Chrome (or an equivalent
browser-automation tool) is the right way to do this in practice. A few
things about how LinkedIn's UI actually behaves make it worth doing a
specific way:

- **Page by URL, not by clicking "Next."** LinkedIn's job search accepts a
  `start` parameter (`start=25`, `start=50`, ...) - navigating it directly is
  far more reliable than repeated pagination clicks, and each page's full
  card list (title, company, location, posted-time, comp if shown) comes back
  cleanly from a single page-text read. Batch a few page loads together in
  one tool round-trip rather than one page per call.
- **The platform's own result count drifts as you page** - it is a live,
  approximate index, not a fixed total. Expect that and don't treat it as an
  error.
- **Opening one listing for a closer look is less reliable via element
  references than via a screenshot and a direct click on the visible card** -
  element-reference clicks on this UI sometimes silently no-op. Take a
  screenshot, click the coordinates, then give the detail pane a moment to
  load before reading it - it renders asynchronously and an early read can
  return the previous listing's content.
- **Treat LinkedIn's own description pane as unreliable, even logged in.**
  Full job descriptions there are frequently truncated behind a "...more"
  toggle or stuck on a loading placeholder that never resolves. Don't fight
  it - the instruction this file already gives for every other discovery
  source applies here without modification: LinkedIn tells you a role
  exists; the employer's own board is where you actually read it and confirm
  it's live.
- **Close every tab opened this way once its listing has been read**, same as
  any other browser-automation task.

**The default operation is one page read of the rendered results list, then
verification on the employer's own board.** Opening the occasional card for a
closer look is fine. Clicking through cards in bulk to harvest ids is not, and
that - not reading a page - is the behaviour that gets accounts restricted. The
account at risk is the person's, mid-search, which is the whole reason this line
sits where it does.

A real example from the search this skill was built from: for one person's
roughly hundred-result weekly search, the full discovery pass - every page,
every card's title and company and posting date - took a handful of batched
tool calls and surfaced several genuinely new leads. Trying to read each
listing's complete description from LinkedIn's own pane, by contrast, cost
proportionally more effort than it returned; the same descriptions came back
complete and reliable moments later, straight from the employer's own board,
which is exactly where they needed to be read from anyway to verify the role
was still live.

**Find the saved search rather than asking for it.** On `linkedin.com/jobs/`
the "Jobs based on your preferences" block carries a **"Show all" link whose
href is the full preferences query** - keywords, `geoId`, origin. One DOM read
gets it; append `distance=25&f_TPR=r86400&sortBy=DD` and that is the daily
search, with no need for the person to paste anything. Reading the href has a
second use: that query string is the only evidence of what the saved search
currently contains, which matters two rules further down.

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

**The posted-age on a card is the repost age, and it must never lift a score.**
Three cards presenting as hours old in one evening were requisitions first
published seven months, ten weeks and six weeks earlier - one of them the
person's own live application, re-promoted. The date that means anything is
`first_published` on the employer's ATS, one read away. Freshness is read from
the ATS, never from the feed; see the decay signals in `07-fit-scoring.md`.

**Its work-mode tag disagrees with the employer's posting.** "On-site" on
LinkedIn was "hybrid, at least half the month" on the same employer's Greenhouse
page. That tag decides an office-days filter, so trust the employer's board over
it, always.

**Three junk classes fill the recommendations feed, and all three are visible
from the list.** Eleven of twelve rows in one read fell into them:

1. **Already decided** - reposts of rows the person archived weeks ago. This is
   the archive earning its keep; triage against it first.
2. **Aggregators and staffing accounts posting under their own name.** The tell
   is one "employer" posting both an AI Product Manager and a Senior Accountant.
   The employer is undisclosed, so the blind-submission rule below applies - skip
   without reading.
3. **The wrong function wearing a nearby title** - "ML Science Manager",
   "Product Owner (UX)", "Product Engineer".

Running the archive check and the employer-name test *before* opening anything
removes most of a feed in about a minute.

**A rule written in a file does not edit the saved search.** Terms that invite
the wrong shape of role were flagged for deletion on one day and were still
producing five off-target rows a scan five days later, because deleting them
requires someone to open LinkedIn. When a scan shows a term is producing only
noise, the action is *"the person edits the saved search today"*, and the next
scan checks that the query string from the "Show all" href actually changed. A
standing filter that only exists in the tracker screens roles after the search
has already spent its budget finding them.

**A local tech job board.** In Dublin that is **Built In Dublin**; most tech
cities have an equivalent (Built In runs several, and there are strong local
boards elsewhere). These are frequently underrated: no login, visible posting
dates, work mode and seniority on the card, readable descriptions, and often an
AI summary per role. In the search this skill was built from, the local board
produced the majority of live applications.

Its weakness is the very top of the seniority band and non-local remote roles -
exactly the gap LinkedIn fills. Run both; they are complementary, not ranked.

Three things about how it behaves, each learned by getting it wrong first:

- **Search by title, never by category.** The category pages tag by *company*,
  not by role - an "artificial intelligence" category returns sales reps at AI
  companies. Use `/jobs?search=<title>&daysSinceUpdated=<N>`, paged with
  `&page=2`.
- **Listing pages are `robots.txt`-disallowed to fetchers and read fine in the
  person's own browser.** The same distinction as LinkedIn: a person reading a
  page is not a crawler hitting an endpoint.
- **One requisition fans out across every suburb.** A single Lead PM req came
  back as eleven rows. Merge on company plus role before counting anything, or
  the source reports several times the volume it actually found.

Removed listings stay up - the same asymmetry the evidence tiers in
`10-verification.md` are built on. Discovery here; verification on the board.

**A cross-company ATS index.** `my.greenhouse.io` searches across every company
using Greenhouse in one place, and Greenhouse postings more often carry published
salary bands than anything else you will see. Smaller volume, high signal.

Its location filter works only with this exact parameter set:

    my.greenhouse.io/jobs/search?query=<title>&location=<City>%2C%20<Country>
      &lat=<lat>&lon=<lon>&location_type=locality&country_short_name=<CC>

or `location=<Country>&location_type=country` for a whole country. The names
that look right - `latitude`, `longitude`, `locationType`, `country` - are
**silently ignored and return global results**, which presents as a working
search full of the wrong roles. Get the real values once by picking the city
from the site's own autocomplete and copying the URL it produces, then save
that URL and re-run it. A direct `fetch()` returns 406; navigate to it and read
the DOM.

**Two more, each with a specific failure mode.**

*Remote-role aggregators* - `jobgether.com/search-offers?location=<country>&keyword=<title>`
is the one this was learned on - are worth running on Principal and Staff titles
only, where the volume is small enough to read whole. One such run surfaced a
role the other three sources did not carry. Three caveats travel with it: the
seniority classifier is unreliable (a Principal req tagged "Junior, 1-2 years"),
the date sort ignores clicks, and "N days ago" is the aggregator's own re-index
date, not the posting date. The employer is usually named; verify on their board
before anything else.

*Filtered boards that gate behind an account* - the former Otta, now
`global.welcometothejungle.com`, is the current example, and note that the
unprefixed `welcometothejungle.com` is a different product entirely. These carry
published bands and good coverage, and **you may not create the account**. The
person creates the profile; after that it is read exactly like LinkedIn, through
their own signed-in session. Until they do, record it in the dead-ends list with
that as the reason, so it is not re-investigated monthly.

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

**Never let an agency submit a CV before they name the client** - and in practice
the line sits earlier than submission: no agency role is scored, tailored for or
answered on rate until the client is named. A sector named without a client is
not a named client. This is the rule that protects the person, and in Ireland it has legal and code-of-practice force -
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
   a deadline is closing. Some boards cannot be read at all without one, and the
   account is always theirs to create, never yours.
6. Standing review of the saved search itself: when a scan shows a keyword is
   producing only noise, the person edits the saved search that day, and the next
   scan confirms the query string changed.

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

**And an aggregator copy is not evidence the function is hired there either.**
An aggregator carried a "Senior AI Product Manager, remote including Ireland"
more than thirty days after it had left the employer's own board; the board
itself - 227 requisitions, eight of them product roles as the positive control -
had every product req in North America. That produces two things to write down,
not one: the ghost listing, and the lane finding *"this employer does not hire
product in this region right now"*. The second is the one that saves time later.

Other dead ends worth recording: sources that return nothing at the target
seniority, employers who never reply, and search lanes (a location, a work mode,
a title) that produced zero live roles across several weeks. A lane that is
structurally empty is a finding, not a run of bad luck - say which one it is.

## Practical gotchas

- **LinkedIn job descriptions are gated.** Search result lists read fine; the
  descriptions frequently do not. Pull the JD from the company's own board.
- **Cross-company ATS search needs its filters set exactly** - see the parameter
  set under the cross-company ATS index above, and check that the first few hits
  are actually in the target location before trusting a result set. A location
  filter that is silently ignored fails in the one direction nobody checks for:
  it returns plenty of results.
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
