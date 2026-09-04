#!/usr/bin/env python3
"""Lint a job-search tracker for the failures that hide in plain sight.

    python3 scripts/tracker_lint.py job-search-tracker-applications.csv
    python3 scripts/tracker_lint.py rows.csv --root ~/job-search
    python3 scripts/tracker_lint.py rows.csv --masthead ~/job-search/tracker.html

Every check here exists because the thing it catches went undetected in a real
search until it had already cost something. None of them are style rules.

  1. A status outside the five-value vocabulary. Seventeen bespoke strings
     accumulated in a fortnight, and anything deciding "live" by matching the
     status against a known set counted every screen, panel and hiring-manager
     round as not applied - the nine most important rows in the file.
  2. An `In process` row with no stage. In process means a named human is
     engaged; if nobody can say who or where, the status is a guess.
  3. A referenced file that does not exist. A path in a row is a promise, and
     one was found broken a day later by a script trying to open it.
  4. A link that is not a link - a placeholder, a search URL, a board root, or
     the row above's URL pasted into this row. All four are clickable and all
     four fail only at the moment someone tries to apply.
  5. An applied or in-process row whose due date has passed. The board lags
     reality and the lag always flatters, because nobody updates a field to
     record that they did nothing.
  6. A masthead dated anything other than today. The top of the tracker is a
     separate input from the rows, nothing regenerates it, and it is the part
     the person reads first.

Exit code is 0 when nothing is found, 1 otherwise. No personal data is read
into anything but stdout.
"""

import argparse
import csv
import datetime as dt
import os
import re
import sys

STATUSES = ["Scored", "Applied", "In process", "Rejected", "Passed"]

LIVE_STATUSES = ("Applied", "In process")

# Shapes that are never a specific posting, however clickable they look.
BAD_LINK_PATTERNS = [
    (re.compile(r"PLACEHOLDER|TODO|TBC|\[NO LINK", re.I),
     "placeholder text left in the link field"),
    (re.compile(r"linkedin\.com/jobs/(search|view)", re.I),
     "a LinkedIn search or view URL, not the employer's own posting"),
    (re.compile(r"[?&](keywords|query|search)=", re.I),
     "a search query, not a posting"),
    (re.compile(r"/jobs/search\b", re.I),
     "a search path, not a posting"),
    (re.compile(r"^https?://[^/]+/(careers|jobs)/?$", re.I),
     "a careers or jobs index root"),
    (re.compile(r"^https?://[^/]*myworkdayjobs\.com/[^/]+/?$", re.I),
     "a Workday tenant root with no job path"),
    (re.compile(r"^https?://(job-boards|boards)\.greenhouse\.io/[^/]+/?$", re.I),
     "a Greenhouse board root with no job path"),
    (re.compile(r"^https?://jobs\.ashbyhq\.com/[^/]+/?$", re.I),
     "an Ashby board root with no job path"),
]

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d %b %Y", "%d %B %Y", "%Y/%m/%d"]

PATH_FIELDS = ["CV used", "File", "Role file", "Cover note"]


def parse_date(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return False        # present, but not machine-readable


def looks_like_path(value):
    v = (value or "").strip()
    if not v or v.startswith(("http://", "https://")):
        return False
    return "/" in v or v.lower().endswith((".md", ".pdf", ".docx", ".txt"))


def row_label(i, row):
    company = (row.get("Company") or "").strip()
    role = (row.get("Role title") or row.get("Role") or "").strip()
    name = " - ".join(x for x in (company, role) if x)
    return f"row {i}" + (f" ({name})" if name else "")


def lint_rows(rows, root, today):
    findings = []
    seen_links = {}

    for i, row in enumerate(rows, start=2):     # 2 = first data row in a sheet
        where = row_label(i, row)

        status = (row.get("Status") or "").strip()
        if status and status not in STATUSES:
            findings.append(
                f"{where}: status {status!r} is not one of the five "
                f"({', '.join(STATUSES)}). Where the process stands goes in Stage.")

        if status == "In process" and not (row.get("Stage") or "").strip():
            findings.append(
                f"{where}: In process with no Stage. Name the human and the round, "
                "or the status is a guess.")

        link = (row.get("JD link") or "").strip()
        if link:
            for pattern, why in BAD_LINK_PATTERNS:
                if pattern.search(link):
                    findings.append(f"{where}: JD link is {why} - {link}")
                    break
            first = seen_links.get(link)
            if first:
                findings.append(
                    f"{where}: JD link is identical to {first}. One of them was "
                    f"copied from the other - {link}")
            else:
                seen_links[link] = where

        for field in PATH_FIELDS:
            value = (row.get(field) or "").strip()
            if looks_like_path(value):
                path = os.path.expanduser(value)
                if not os.path.isabs(path):
                    path = os.path.join(root, path)
                if not os.path.exists(path):
                    findings.append(
                        f"{where}: {field} points at {value!r}, which does not "
                        "exist. A path in a row is a promise.")

        due = parse_date(row.get("Due"))
        if due is False:
            findings.append(
                f"{where}: due date {row.get('Due')!r} is not a readable date. "
                "Dates come from the clock, in a format something can parse.")
        elif due and due < today and status in LIVE_STATUSES:
            days = (today - due).days
            findings.append(
                f"{where}: {status}, due {due.isoformat()} - {days} day(s) ago. "
                "Either it was done and the row was never updated, or it was not "
                "done. Ask which before advising on this row.")

    return findings


def lint_masthead(path, today):
    """The header is a separate input from the rows and nothing regenerates it."""
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as fh:
            head = fh.read(4000)
    except OSError as e:
        return [f"masthead: could not read {path} ({e})"]

    stamps = {
        today.isoformat(),
        f"{today.day} {today.strftime('%b')}",
        f"{today.day} {today.strftime('%B')}",
        today.strftime("%d/%m/%Y"),
    }
    if any(stamp in head for stamp in stamps):
        return []
    return [
        f"masthead: no occurrence of today's date ({today.isoformat()}) in the "
        f"first 4000 characters of {path}. The top of the tracker is the part "
        "read first and the part nothing rebuilds - set it from the clock and "
        "re-derive the three actions from priority, not from what they were."
    ]


def main():
    ap = argparse.ArgumentParser(description="Lint a job-search tracker.")
    ap.add_argument("csv_path", help="the applications tab, exported as CSV")
    ap.add_argument("--root", default=".",
                    help="directory that relative file paths are resolved against")
    ap.add_argument("--masthead",
                    help="rendered tracker or digest whose header date is checked")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    args = ap.parse_args()

    today = (dt.date.fromisoformat(args.today) if args.today
             else dt.date.today())

    path = os.path.expanduser(args.csv_path)
    if not os.path.exists(path):
        print(f"Not found: {path}")
        return 2

    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    rows = [r for r in rows
            if "EXAMPLE" not in (r.get("Company") or "").upper()]

    findings = lint_rows(rows, os.path.expanduser(args.root), today)
    if args.masthead:
        findings += lint_masthead(args.masthead, today)

    print(f"\nTracker lint: {os.path.basename(path)} - {len(rows)} row(s), "
          f"today {today.isoformat()}")
    print("=" * 60)
    if findings:
        for f in findings:
            print(f"  [FLAG] {f}")
        print("=" * 60)
        print(f"FAILED - {len(findings)} finding(s).")
        return 1
    print("PASSED - statuses canonical, links specific, files present, "
          "nothing silently overdue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
