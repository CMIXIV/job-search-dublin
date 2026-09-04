#!/usr/bin/env python3
"""Generate a job-search tracker.

Writes an .xlsx workbook (Applications, Contacts, Source summary) and CSV
exports of each tab, so the same schema can be imported into Google Sheets,
Notion or Airtable.

Usage:
    python3 make_tracker.py                     # -> ./job-search-tracker.xlsx + CSVs
    python3 make_tracker.py --out ~/job-search  # choose a directory
    python3 make_tracker.py --csv-only          # skip the xlsx (no openpyxl needed)

No personal data is embedded. One example row is included and marked EXAMPLE -
delete it once real roles are added.
"""

import argparse
import csv
import os
import sys

APPLICATIONS = [
    "Rank", "Date found", "Source", "Company", "Role title", "Band", "Depth",
    "Via", "Consent",
    "Location / mode", "JD link", "Posted", "Salary band",
    "Fit", "Probability", "Priority",
    "Why", "Watch", "Route", "Advocate",
    "Status", "Stage", "Date applied", "Next action", "Due", "CV used", "Notes",
]

# Where a listing hides the employer, Company reads
# "[EMPLOYER NOT DISCLOSED]" and Via names the agency. Never guess the employer -
# two hidden listings are often the same underlying role, and a guess makes that
# undetectable.
CONSENT = [
    "Direct - n/a",
    "Asked, awaiting client name",
    "Consent given",
    "Consent withheld",
    "SUBMITTED WITHOUT CONSENT",
]

HISTORY = [
    "Company", "Role", "Level", "Date", "Stage reached", "Outcome", "Feedback",
    "Notes",
]

CONTACTS = [
    "Name", "Company", "Relationship", "How they can help", "Asked on",
    "Last contact", "Next follow-up", "Status", "Notes",
]

SOURCES = ["Source", "Roles found", "Applications", "In process", "Rejected",
           "Offers"]

# Status is a bucket of exactly five values; where a process actually stands is
# a sentence, and it goes in Stage. A real tracker's status column reached
# seventeen bespoke strings in a fortnight, and anything deciding "live" by
# matching Status against a known set then counted every screen, panel and
# hiring-manager round as not applied. The data validation below is what stops
# the eighteenth string being typed.
#
# Rejected (they declined you) and Passed (you declined them, or closed a dead
# application at day 30) are deliberately distinct - the Passed rows are where
# your screening filters come from.
STATUSES = ["Scored", "Applied", "In process", "Rejected", "Passed"]

# Stage is free text and deliberately un-validated. It should read like a state
# someone can act on: "Screen confirmed Wed 09:00", "Panel held, awaiting
# outcome", "Escalation live - introduction made", "Offer verbal, written
# pending", "Agency submitted, client named".

DEPTHS = ["High", "Medium", "Low"]

BANDS = ["Mid", "Senior", "Lead", "Staff", "Principal", "Director", "VP", "Other"]

DEFAULT_SOURCES = [
    "LinkedIn", "Local job board", "Greenhouse (my.greenhouse.io)",
    "Company board", "Referral", "Recruiter", "Other",
]

EXAMPLE_ROW = [
    "1", "2026-08-16", "LinkedIn", "EXAMPLE - delete this row",
    "Senior Product Manager", "Senior", "High", "", "Direct - n/a",
    "Dublin / hybrid 2d", "https://",
    "req 12345, posted 6 days ago", "",
    "8", "6", "",
    "Core of the role is the thing I am best at, not a bolt-on",
    "They name a tool I have never used - do not blur it with the adjacent one",
    "Direct application, no route in yet", "",
    "Scored", "", "", "Read full JD and re-score", "2026-08-18", "", "",
]


def write_csvs(out_dir):
    paths = []
    for name, header, rows in (
        ("applications", APPLICATIONS, [EXAMPLE_ROW]),
        ("contacts", CONTACTS, []),
        ("interview-history", HISTORY, []),
        ("source-summary", SOURCES, [[s, "", "", "", "", ""] for s in DEFAULT_SOURCES]),
    ):
        path = os.path.join(out_dir, f"job-search-tracker-{name}.csv")
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(header)
            writer.writerows(rows)
        paths.append(path)
    return paths


def write_xlsx(out_dir):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
        from openpyxl.worksheet.datavalidation import DataValidation
    except ImportError:
        print("openpyxl not installed - run 'pip install openpyxl' or use --csv-only")
        return None

    wb = Workbook()
    head_font = Font(bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", fgColor="2F4858")

    def style_header(ws, header, widths):
        """widths is keyed by column *name*. Keying it by position was the same
        mistake the formula column letters below already document: inserting a
        column silently repoints every entry after it."""
        ws.append(header)
        for i, name in enumerate(header, start=1):
            cell = ws.cell(row=1, column=i)
            cell.font = head_font
            cell.fill = head_fill
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            ws.column_dimensions[get_column_letter(i)].width = widths.get(name, 16)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = f"A1:{get_column_letter(len(header))}1"

    ws = wb.active
    ws.title = "Applications"
    style_header(ws, APPLICATIONS, {
        "Company": 22, "Role title": 28, "Via": 20, "Consent": 26,
        "Location / mode": 22, "JD link": 30, "Posted": 24,
        "Why": 40, "Watch": 40, "Route": 30, "Stage": 34,
        "Next action": 30, "Notes": 34})
    ws.append(EXAMPLE_ROW)

    # Column letters are derived from APPLICATIONS, never hard-coded - inserting
    # a column silently repointed every one of these the last time they were.
    col = {name: get_column_letter(i)
           for i, name in enumerate(APPLICATIONS, start=1)}

    status_dv = DataValidation(type="list", formula1='"%s"' % ",".join(STATUSES), allow_blank=True)
    depth_dv = DataValidation(type="list", formula1='"%s"' % ",".join(DEPTHS), allow_blank=True)
    band_dv = DataValidation(type="list", formula1='"%s"' % ",".join(BANDS), allow_blank=True)
    source_dv = DataValidation(type="list", formula1='"%s"' % ",".join(DEFAULT_SOURCES), allow_blank=True)
    consent_dv = DataValidation(type="list", formula1='"%s"' % ",".join(CONSENT), allow_blank=True)
    score_dv = DataValidation(type="whole", operator="between", formula1=1, formula2=10, allow_blank=True)
    for dv in (status_dv, band_dv, source_dv, score_dv, depth_dv, consent_dv):
        ws.add_data_validation(dv)
    status_dv.add(f"{col['Status']}2:{col['Status']}500")
    band_dv.add(f"{col['Band']}2:{col['Band']}500")
    depth_dv.add(f"{col['Depth']}2:{col['Depth']}500")
    source_dv.add(f"{col['Source']}2:{col['Source']}500")
    consent_dv.add(f"{col['Consent']}2:{col['Consent']}500")
    score_dv.add(f"{col['Fit']}2:{col['Fit']}500")
    score_dv.add(f"{col['Probability']}2:{col['Probability']}500")

    # Priority = Fit and Probability weighted equally. Overwrite by hand when
    # comp or title justifies an adjustment, and say so in the Why column.
    f, pr = col["Fit"], col["Probability"]
    for r in range(2, 501):
        ws.cell(row=r, column=APPLICATIONS.index("Priority") + 1,
                value=f'=IF(COUNT({f}{r}:{pr}{r})=2,AVERAGE({f}{r}:{pr}{r}),"")')

    ws_c = wb.create_sheet("Contacts")
    style_header(ws_c, CONTACTS, {"How they can help": 30, "Notes": 34})

    ws_h = wb.create_sheet("Interview history")
    style_header(ws_h, HISTORY, {"Stage reached": 22, "Feedback": 40, "Notes": 34})

    ws_s = wb.create_sheet("Source summary")
    style_header(ws_s, SOURCES, {"Source": 28})
    for i, src in enumerate(DEFAULT_SOURCES, start=2):
        ws_s.cell(row=i, column=1, value=src)
        src_c, app_c, st_c = col["Source"], col["Date applied"], col["Status"]
        ws_s.cell(row=i, column=2, value=(
            f'=COUNTIF(Applications!${src_c}$2:${src_c}$500,$A{i})'))
        ws_s.cell(row=i, column=3, value=(
            f'=COUNTIFS(Applications!${src_c}$2:${src_c}$500,$A{i},'
            f'Applications!${app_c}$2:${app_c}$500,"<>")'
        ))
        for c, status in ((4, "In process"), (5, "Rejected")):
            ws_s.cell(row=i, column=c, value=(
                f'=COUNTIFS(Applications!${src_c}$2:${src_c}$500,$A{i},'
                f'Applications!${st_c}$2:${st_c}$500,"{status}")'
            ))
        # Offer is a stage of In process, not a status - count it from the text.
        stg_c = col["Stage"]
        ws_s.cell(row=i, column=6, value=(
            f'=COUNTIFS(Applications!${src_c}$2:${src_c}$500,$A{i},'
            f'Applications!${stg_c}$2:${stg_c}$500,"*offer*")'
        ))
    note_row = len(DEFAULT_SOURCES) + 3
    ws_s.cell(row=note_row, column=1,
              value="Applications counts rows with a 'Date applied'. In process and "
                    "Rejected count current status only. Offers matches the word "
                    "'offer' in the Stage column, because Offer is a stage of In "
                    "process, not a status of its own. Compare warm routes "
                    "(Advocate filled) against cold ones at least monthly.")

    path = os.path.join(out_dir, "job-search-tracker.xlsx")
    wb.save(path)
    return path


def main():
    ap = argparse.ArgumentParser(description="Generate a job-search tracker.")
    ap.add_argument("--out", default=".", help="output directory (default: current)")
    ap.add_argument("--csv-only", action="store_true", help="skip the xlsx")
    args = ap.parse_args()

    out_dir = os.path.expanduser(args.out)
    os.makedirs(out_dir, exist_ok=True)

    written = write_csvs(out_dir)
    if not args.csv_only:
        xlsx = write_xlsx(out_dir)
        if xlsx:
            written.insert(0, xlsx)

    print("Wrote:")
    for p in written:
        print("  " + p)
    print("\nGoogle Sheets: File > Import > Upload the applications CSV, then repeat "
          "for each of the other CSVs as new tabs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
