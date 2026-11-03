#!/usr/bin/env python3
"""Regression check for the phase-7 verification protocol.

Exercises the verdict rules in references/10-verification.md against a small
set of fixtures before a verification sweep is trusted. Run it after touching
that file, this script, or the escalation logic it encodes.

    python3 scripts/verify_check.py

Exit code is 0 if every assertion holds, 1 if anything fails. It fails loudly:
a broken assertion prints what was expected, what happened, and which rule it
maps to. It does not warn and continue.

Two kinds of fixture:

  - LIVE fixtures (assertions 1-3, 5) hit a real, public Greenhouse board -
    Greenhouse's own careers board, chosen because it is the ATS vendor
    hiring on its own product and about as durable a public fixture as
    exists. These test real network behaviour: a real single-record lookup,
    a real listing, a real wrong-token 404.

  - LOCAL fixtures (assertions 4, 6-15) are recorded payloads, not live
    calls. They exist to pin down structural cases - a truncated listing, a
    summarising read, a partial Ashby board, an emitter that closes
    everything, a location twin, an evergreen requisition id, a country past
    the cut of a truncated location string, a pay tier that clears where the
    summary range does not - that a live public board cannot be relied on to
    keep reproducing on demand. Their figures are invented.

A note on how the real reads are meant to be made, because it is the thing
these fixtures are protecting. A board listing settles liveness only when it
is read deterministically: navigate a browser to the API URL, parse the body,
filter in code. A summarising fetch tool reported "164 jobs, id not present"
on a board that held 309 and did contain the id - it did not fail, it
summarised, and a summary of a list is not a list. Greenhouse's /jobs also
truncates past roughly 300 requisitions, so use ?content=false or the
per-office and per-department endpoints on large boards. The fetch tool is
for ranking; it never closes a role. See references/10-verification.md.

Fixture rot. The live fixtures will eventually break: a job closes, a board
gets renamed, an API shape changes. That is expected and is not a reason to
weaken an assertion or delete a check - it is the check doing its job. When a
live fixture stops behaving as recorded, replace the fixture (a current job
id, a current wrong-token string that still 404s) and keep the assertion.
Weakening what GONE requires to make an old fixture pass again is exactly the
failure this file exists to catch.

No personal data. Every identifier below is public ATS metadata unconnected
to any person's job search - see the anonymisation note in README.md.
"""

import json
import sys
import urllib.error
import urllib.request

TIMEOUT = 15

BOARD_TOKEN = "greenhouse"           # Greenhouse's own careers board
LIVE_JOB_ID = 6180015                # confirmed open at recording time
DEAD_JOB_ID = 1                      # permanently invalid - ids are large auto-increments
WRONG_TOKEN = "this-token-does-not-exist-zzz"

FAILURES = []


def check(label, rule, condition, detail):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label} ({rule})")
    if not condition:
        print(f"       {detail}")
        FAILURES.append(label)
    return condition


# ---------------------------------------------------------------------------
# Network primitives
# ---------------------------------------------------------------------------

def fetch(url):
    """Return (status_code, payload). status is None only on a network failure,
    never on an HTTP error - a 404 is a valid, reachable answer."""
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "job-search-agent-verify-selfcheck/1.0"}
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            try:
                return resp.status, json.loads(body)
            except json.JSONDecodeError:
                return resp.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except (urllib.error.URLError, OSError):
        return None, None


def single_record(token, job_id):
    """True = found, False = confirmed absent (404), None = unreachable."""
    status, payload = fetch(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs/{job_id}")
    if status == 200 and payload:
        return True
    if status == 404:
        return False
    return None


def board_listing(token):
    """List of job ids on the board, or None if the board could not be read."""
    status, payload = fetch(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=false")
    if status == 200 and isinstance(payload, dict) and isinstance(payload.get("jobs"), list):
        return [j["id"] for j in payload["jobs"]]
    return None


# ---------------------------------------------------------------------------
# Verdict logic under test - mirrors references/10-verification.md 1.1 / 1.4
# ---------------------------------------------------------------------------

def verdict(found, control_ids):
    """
    found: True/False/None from single_record().
    control_ids: ids confirmed present on the same board this session, or a
    falsy value if no working positive control was obtained.

    GONE is reachable only through found=False AND a non-empty control. Every
    other combination - including found=False with no control - is UNVERIFIED.
    This is the whole D1/D2 fix in one function.
    """
    if found is True:
        return "LIVE"
    if found is False and control_ids:
        return "GONE"
    return "UNVERIFIED"


def verdict_from_listing(target_id, records_read, declared_total,
                         deterministic=True):
    """references/10-verification.md 1.3 and the summarising-read rule: a
    not-found result from a listing is UNVERIFIED unless the listing can be
    shown complete (declared total matches records actually read) *and* the
    read was deterministic.

    deterministic=False means the listing came back through a tool that
    summarises - which is free to report a total it did not count. Such a read
    can establish LIVE (a record it did surface is a record that exists) but
    can never establish absence, whatever total it claims.
    """
    if target_id in records_read:
        return "LIVE"
    if not deterministic:
        return "UNVERIFIED"
    complete = declared_total is not None and declared_total == len(records_read)
    return "GONE" if complete else "UNVERIFIED"


def tier_b_is_trusted(source_history):
    """references/10-verification.md 1.6: a source that has claimed closure on
    a requisition Tier A confirms live is an unreliable emitter."""
    return not source_history.get("claimed_closed_on_a_tier_a_live_id", False)


def effective_tier(claimed_tier, source, false_emitters):
    """A closure statement is Tier B only from a source not on the confirmed
    false-emitter list. From a listed emitter it is Tier C, which settles
    nothing - including when the emitter is the employer's own careers site.
    Each entry on that list carries the control that proved it."""
    if claimed_tier == "B" and source in false_emitters:
        return "C"
    return claimed_tier


def location_verdict(tag_city, body_city, twin_count):
    """The location-twins rule: a location tag is a claim, not a fact. Where a
    requisition exists as several location twins, or where the description body
    names a different city from the tag, the location is UNVERIFIED until the
    employer answers - and the twins count as one hire, not N."""
    if body_city and tag_city and body_city.strip().lower() != tag_city.strip().lower():
        return "UNVERIFIED"
    if twin_count > 1:
        return "UNVERIFIED"
    return "LIVE"


REGION_ONLY = ("europe", "emea", "remote - europe", "remote-europe", "remote, europe")


def all_locations(posting, platform):
    """10-verification.md, read the location list in full: every location the
    ATS publishes for a posting, untruncated. Slicing is for display only."""
    if platform == "ashby":
        locs = [posting.get("location")]
        locs += [s.get("location") for s in posting.get("secondaryLocations") or []]
        tiers = (posting.get("compensation") or {}).get("compensationTiers") or []
        locs += [t.get("title") for t in tiers]
    elif platform == "greenhouse":
        locs = [(posting.get("location") or {}).get("name")]
        locs += [o.get("name") for o in posting.get("offices") or []]
    elif platform == "lever":
        cats = posting.get("categories") or {}
        locs = [cats.get("location")] + list(cats.get("allLocations") or [])
    elif platform == "workday":
        info = posting.get("jobPostingInfo") or posting
        locs = [info.get("location")] + list(info.get("additionalLocations") or [])
    else:
        raise ValueError(f"unknown platform {platform!r}")
    return [l for l in locs if l]


def country_eligibility(posting, platform, needles):
    """ELIGIBLE on any match across the full list; UNVERIFIED where the only
    location is a region with no country list; NOT ELIGIBLE otherwise."""
    locs = all_locations(posting, platform)
    wanted = [n.lower() for n in needles]
    if any(n in l.lower() for l in locs for n in wanted):
        return "ELIGIBLE"
    if not locs or all(l.strip().lower() in REGION_ONLY for l in locs):
        return "UNVERIFIED"
    return "NOT ELIGIBLE"


def country_pay(posting, country, floor):
    """07-fit-scoring.md, per-country tiers: where tiers are published the floor
    is tested against the tier for the person's country, never the summary.
    Returns (verdict, (low, high) or None)."""
    tiers = (posting.get("compensation") or {}).get("compensationTiers") or []
    if not tiers:
        return "NO TIERS", None
    for t in tiers:
        if country.lower() in (t.get("title") or "").lower():
            salary = [c for c in t.get("components") or []
                      if c.get("compensationType") == "Salary"]
            if not salary:
                return "UNKNOWN", None
            low, high = salary[0]["minValue"], salary[0]["maxValue"]
            if low >= floor:
                return "CLEARS", (low, high)
            if high < floor:
                return "BELOW", (low, high)
            return "STRADDLES", (low, high)
    return "UNKNOWN", None


def verdict_with_tiers(tier_a_verdict, tier_b_claims_closed, source_history):
    """Tier A settles it outright when available. Tier B only settles GONE, and
    only from a source that has passed the trust check above."""
    if tier_a_verdict in ("LIVE", "GONE"):
        return tier_a_verdict
    if tier_b_claims_closed and tier_b_is_trusted(source_history):
        return "GONE"
    return "UNVERIFIED"


def apply_decay(role):
    """references/07-fit-scoring.md decay section: adjusts Probability only,
    Fit is returned untouched."""
    fit = role["fit"]
    probability = role["probability"]
    reasons = []

    if role.get("evergreen_requisition_id"):
        probability = min(probability, 3)
        reasons.append("evergreen requisition id - heavy cut regardless of fit")
    else:
        weeks = role.get("age_weeks", 0)
        if weeks > 12:
            probability = max(0, probability - 4)
            reasons.append("posted beyond ~3 months - heavy cut")
        elif weeks > 6:
            probability = max(0, probability - 2)
            reasons.append("posted beyond ~6 weeks - visible cut")

    if role.get("applicant_count", 0) >= 100:
        probability = max(0, probability - 2)
        reasons.append("applicant count in the hundreds - cut")

    return fit, probability, reasons


# ---------------------------------------------------------------------------
# Assertions
# ---------------------------------------------------------------------------

def run():
    live_found = single_record(BOARD_TOKEN, LIVE_JOB_ID)
    check(
        "1. single-record lookup on the live fixture returns a record",
        "1.1 LIVE",
        live_found is True,
        f"single_record({BOARD_TOKEN}, {LIVE_JOB_ID}) returned {live_found!r}, "
        "expected True. The fixture job id may have closed - if so this is "
        "fixture rot: replace LIVE_JOB_ID with a currently-open id on the "
        "same board, do not weaken this assertion.",
    )

    dead_found = single_record(BOARD_TOKEN, DEAD_JOB_ID)
    check(
        "2. single-record lookup on the dead fixture fails",
        "1.1 GONE precondition",
        dead_found is False,
        f"single_record({BOARD_TOKEN}, {DEAD_JOB_ID}) returned {dead_found!r}, expected False.",
    )

    control_ids = board_listing(BOARD_TOKEN)
    check(
        "3. the board listing in the same session returns records - the positive control",
        "1.4 positive control",
        bool(control_ids),
        f"board_listing({BOARD_TOKEN}) returned {control_ids!r}, expected a non-empty list. "
        "If the board is genuinely down right now, re-run later rather than weakening "
        "assertion 4's requirement for a control.",
    )

    gone_with_control = verdict(dead_found, control_ids)
    gone_without_control = verdict(dead_found, [])
    check(
        "4. GONE is emitted only when 2 and 3 both hold (D1 regression)",
        "1.1 / 1.4",
        gone_with_control == "GONE" and gone_without_control == "UNVERIFIED",
        f"verdict(found=False, control=<real>) = {gone_with_control!r} (want GONE); "
        f"verdict(found=False, control=[]) = {gone_without_control!r} (want UNVERIFIED).",
    )

    wrong_token_found = single_record(WRONG_TOKEN, LIVE_JOB_ID)
    wrong_token_control = board_listing(WRONG_TOKEN)
    wrong_token_verdict = verdict(wrong_token_found, wrong_token_control)
    check(
        "5. the wrong-token fixture yields UNVERIFIED, never GONE (D4)",
        "1.5",
        wrong_token_verdict == "UNVERIFIED",
        f"verdict on token {WRONG_TOKEN!r} = {wrong_token_verdict!r}, expected UNVERIFIED. "
        f"(found={wrong_token_found!r}, control={wrong_token_control!r})",
    )

    truncated_verdict = verdict_from_listing(
        target_id="req-not-in-the-first-page",
        records_read=[f"rec-{i}" for i in range(100)],
        declared_total=500,
    )
    check(
        "6. an id absent from the truncated-listing fixture yields UNVERIFIED, never GONE (D1)",
        "1.3",
        truncated_verdict == "UNVERIFIED",
        f"verdict_from_listing(...) = {truncated_verdict!r}, expected UNVERIFIED "
        "(100 of a declared 500 read is not a complete listing).",
    )

    unreliable_source = {"claimed_closed_on_a_tier_a_live_id": True}
    emitter_verdict = verdict_with_tiers(
        tier_a_verdict="LIVE",
        tier_b_claims_closed=True,
        source_history=unreliable_source,
    )
    check(
        "7. a closure statement from the unreliable-emitter fixture, on a record "
        "the ATS confirms live, does not yield GONE (D3, rule 1.6)",
        "1.6",
        emitter_verdict != "GONE" and not tier_b_is_trusted(unreliable_source),
        f"verdict_with_tiers(...) = {emitter_verdict!r}, expected LIVE (Tier A settles it); "
        f"tier_b_is_trusted(...) = {tier_b_is_trusted(unreliable_source)!r}, expected False.",
    )

    summarised_verdict = verdict_from_listing(
        target_id="req-12345",
        records_read=[f"rec-{i}" for i in range(164)],
        declared_total=164,
        deterministic=False,
    )
    check(
        "8. a summarising read reporting a self-consistent total yields "
        "UNVERIFIED, never GONE",
        "10-verification.md, a summary is not a read",
        summarised_verdict == "UNVERIFIED",
        f"verdict_from_listing(deterministic=False) = {summarised_verdict!r}, "
        "expected UNVERIFIED. A tool that summarises can report a total it did "
        "not count - 164 was reported on a board holding 309 - so its total "
        "matching its own record count proves nothing.",
    )

    ashby_verdict = verdict_from_listing(
        target_id="req-not-in-the-partial-payload",
        records_read=[f"ashby-{i}" for i in range(8)],
        declared_total=37,          # what the rendered board showed
    )
    check(
        "9. an id absent from the partial-Ashby fixture yields UNVERIFIED, "
        "never GONE",
        "10-verification.md, listings known to come back partial",
        ashby_verdict == "UNVERIFIED",
        f"verdict_from_listing(...) = {ashby_verdict!r}, expected UNVERIFIED "
        "(8 records against a rendered board of 37 is a partial listing, and "
        "Ashby's posting API returns these intermittently).",
    )

    twin_location = location_verdict(
        tag_city="Dublin",
        body_city="Berlin",        # the description body names a different city
        twin_count=3,
    )
    check(
        "10. a location twin whose description body names a different city "
        "yields an UNVERIFIED location",
        "10-verification.md, location tags are claims",
        twin_location == "UNVERIFIED",
        f"location_verdict(...) = {twin_location!r}, expected UNVERIFIED. A "
        "location tag must not clear a location filter on its own where the "
        "body names another city, and N twins are one hire.",
    )

    false_emitters = {"employer-careers-site"}
    demoted = effective_tier("B", "employer-careers-site", false_emitters)
    kept = effective_tier("B", "some-other-board", false_emitters)
    check(
        "11. a closure statement from a listed false emitter is demoted to "
        "Tier C, and one from an unlisted source is not",
        "1.6 / confirmed false-emitter list",
        demoted == "C" and kept == "B",
        f"effective_tier(listed) = {demoted!r} (want C); "
        f"effective_tier(unlisted) = {kept!r} (want B).",
    )

    evergreen_role = {
        "fit": 8,
        "probability": 7,
        "evergreen_requisition_id": True,
        "age_weeks": 2,
        "applicant_count": 20,
    }
    fit_out, probability_out, reasons = apply_decay(evergreen_role)
    check(
        "12. a fixture carrying an evergreen requisition id produces a Probability "
        "penalty and leaves Fit unchanged (D5)",
        "07-fit-scoring.md decay section",
        fit_out == evergreen_role["fit"] and probability_out < evergreen_role["probability"] and reasons,
        f"apply_decay(...) = fit {fit_out}, probability {probability_out}, reasons {reasons!r}. "
        f"Expected fit unchanged at {evergreen_role['fit']} and probability below "
        f"{evergreen_role['probability']}.",
    )

    # The shape of the Ashby incident, with invented figures: the person's country is the last
    # of 28 locations, past the point where a joined string was cut.
    countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
                 "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
                 "Hungary", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta",
                 "Netherlands", "Norway", "Poland", "Romania", "Slovakia",
                 "Slovenia", "Spain", "Sweden", "Switzerland", "Portugal"]
    ashby_posting = {
        "location": "Remote - Europe",
        "secondaryLocations": [{"location": c} for c in countries],
        "compensation": {
            "compensationTierSummary": "€80K – €150K",
            "compensationTiers": [
                {"title": "Tier 2 - Eastern Europe",
                 "components": [{"compensationType": "Salary",
                                 "minValue": 80000, "maxValue": 110000}]},
                {"title": "Tier 1 - Portugal, Netherlands",
                 "components": [{"compensationType": "Salary",
                                 "minValue": 125000, "maxValue": 150000}]},
            ],
        },
    }
    joined = ", ".join(all_locations(ashby_posting, "ashby"))
    truncated_hit = "portugal" in joined[:100].lower()
    full_hit = country_eligibility(ashby_posting, "ashby", ["Portugal"])
    check(
        "13. a country past the 100th character of the location list is still "
        "matched (truncation regression)",
        "10-verification.md, read the location list in full",
        not truncated_hit and full_hit == "ELIGIBLE",
        f"country_eligibility(...) = {full_hit!r}, expected ELIGIBLE. The "
        f"fixture's country sits at character {joined.lower().find('portugal')} of "
        f"{len(joined)}; if truncated_hit ({truncated_hit!r}) is True the "
        "fixture no longer exercises the cut - lengthen it, do not drop the check.",
    )

    gh_posting = {"location": {"name": "Berlin"},
                  "offices": [{"name": "Berlin"}, {"name": "Lisbon"}]}
    gh_hit = country_eligibility(gh_posting, "greenhouse", ["Portugal", "Lisbon"])
    region_only = country_eligibility({"location": "Remote - Europe"}, "ashby",
                                      ["Portugal"])
    check(
        "14. a Greenhouse office past location.name clears, and a region with no "
        "country list is UNVERIFIED, never NOT ELIGIBLE",
        "10-verification.md, read the location list in full",
        gh_hit == "ELIGIBLE" and region_only == "UNVERIFIED",
        f"greenhouse offices[] = {gh_hit!r} (want ELIGIBLE); "
        f"region only = {region_only!r} (want UNVERIFIED).",
    )

    pay, band = country_pay(ashby_posting, "Portugal", floor=115000)
    no_tier, _ = country_pay(ashby_posting, "Ireland", floor=115000)
    check(
        "15. the floor is tested against the country tier, not the summary "
        "range, and a missing country tier is UNKNOWN",
        "07-fit-scoring.md, per-country tiers",
        pay == "CLEARS" and band == (125000, 150000) and no_tier == "UNKNOWN",
        f"country_pay(Portugal) = {pay!r} {band!r} (want CLEARS (125000, 150000)); "
        f"country_pay(no tier) = {no_tier!r} (want UNKNOWN). The summary's "
        "bottom is under the floor; it must not decide the verdict.",
    )

    total = 15
    print()
    if FAILURES:
        print(f"{len(FAILURES)} of {total} checks failed: {', '.join(FAILURES)}")
        return 1
    print(f"{total} of {total} checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
