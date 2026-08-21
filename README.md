# Job Search Agent

A skill for running an end-to-end job search — from a standing start to a signed
offer.

Built by and for people job-hunting in Dublin's tech sphere, but it works for
any city or industry. It encodes what actually worked: interviewing people for
the strengths their CVs undersell, challenging target job titles against real
evidence, one master CV tailored per role, a source stack that is measured
rather than assumed, and a tracker that records where every application came
from.

It is free, it runs inside your own agent session, and none of your data leaves
your machine.

## What it does

1. **Intake** — reads your CV and LinkedIn as *evidence, not truth*, then
   interviews you for the achievements the documents undersell. Pushes for real
   numbers. Never invents one.
2. **Priorities** — runway in months, employment type, visa, location, comp floor,
   and target titles. Then challenges the titles against your evidence, in both
   directions — most people aim too low, some aim too high.
3. **Master CV** — one source of truth, ATS-verified by extracting the text back
   out of the rendered file, then cut down per role in minutes.
4. **Sources** — LinkedIn, your local tech job board, `my.greenhouse.io`, and
   per-employer alerts on Workday, Ashby and Lever. Set up with alerts so
   discovery happens without you remembering to look.
5. **Tracker** — Google Sheets, a local spreadsheet, Notion, Airtable — your
   choice. Source attribution built in from row one, so you can see which source
   is actually producing applications rather than guessing.
6. **Cadence and autonomy** — manual, scheduled discovery, or scheduled discovery
   with applications drafted and staged for review. You always press submit.
7. **Score, apply, follow up** — separate 1–10 scores for Fit (does this match
   what you've shipped) and Probability (honest odds of landing it), combined
   into a Priority that orders your week. Plus cover notes, referral messages, a
   follow-up ladder that ends, and rejection-pattern analysis.

Plus an **Ireland module**: statutory entitlements, minimum notice, collective
consultation, tax on termination payments, Jobseeker's Pay-Related Benefit, and
what employment permit holders need to do first.

## Install

Every route below installs the same thing: a folder named `job-search-agent`
containing `SKILL.md`. Pick whichever suits your tool.

**Claude Desktop (Cowork)** — open
[`dist/job-search-agent.skill`](https://github.com/CMIXIV/job-search-dublin/blob/main/dist/job-search-agent.skill)
and click **Download raw file** (the download icon at the top right of the file
view). Clicking the filename alone opens a web page instead of downloading the
file — that is the most common reason this step fails. Then drag the downloaded
`.skill` file into a chat and click **Save skill**.

The same file is attached to each
[Release](https://github.com/CMIXIV/job-search-dublin/releases) if you prefer.

**claude.ai** — Settings → Capabilities → Skills → Upload, using
[`dist/job-search-agent.zip`](https://github.com/CMIXIV/job-search-dublin/blob/main/dist/job-search-agent.zip).
Identical archive to the `.skill`; that form only accepts a `.zip`.

**Claude Code**

    git clone https://github.com/CMIXIV/job-search-dublin.git \
      ~/.claude/skills/job-search-agent

**Codex CLI** — clone the repo, then either reference it from your project's
`AGENTS.md` (e.g. "read `job-search-agent/SKILL.md` and follow it") or install
it as a custom prompt so it is available as a slash command:

    git clone https://github.com/CMIXIV/job-search-dublin.git \
      ~/.codex/prompts/job-search-agent

**Hermes (via Ollama or any local runner)** — Hermes has no built-in skills
mechanism, so load `SKILL.md` and the files under `references/` as the system
prompt. With a `Modelfile`:

    FROM hermes3
    SYSTEM """
    <paste the contents of SKILL.md and references/*.md here>
    """

then `ollama create job-search-agent -f Modelfile` and run
`ollama run job-search-agent`. Any other agent that can read files and follow
a system prompt works the same way — point it at this repo and have it read
`SKILL.md` first.

Then just say what you need:

> Help me start a job search.
> Is this role worth applying to? [paste the job description]
> Tailor my CV to this spec.
> What am I actually entitled to if I leave this job?

### If something goes wrong

**The Releases link 404s or the page is empty.** No release has been published
yet, or you followed a relative link from the file view. The `dist/` links above
do not depend on releases at all.

**Cowork shows no "Save skill" button.** The download was renamed, or the `.zip`
was used. That button only appears for a `.skill` extension — rename it back and
drag it in again.

**Your agent cannot find the repo.** The repository is `job-search-dublin`; the
skill inside it is `job-search-agent`. They are deliberately different names.

**Maintainers — after changing `SKILL.md`, `references/` or anything else:**

    bash scripts/build_bundle.sh

then commit the regenerated `dist/` files. The bundle is a snapshot of the repo,
so it goes stale the moment the source changes and is not rebuilt. Publishing a
release (`git tag v1.1.0 && git push origin v1.1.0`) rebuilds it automatically
via `.github/workflows/release.yml`.

## What it creates

Everything lives in a `job-search/` folder inside whatever folder you connect:

    job-search/
      00-state.md            where you got to, and every decision made
      01-profile.md          your provable claims, with the numbers
      02-priorities.md       runway, titles, constraints
      03-master-cv.md/.docx  source of truth + generated, ATS-checked
      04-sources.md          configured sources and alerts
      applications/          per role: the JD, the score, the exact CV sent

## Scripts

    python3 scripts/make_tracker.py --out ~/job-search
    python3 scripts/ats_check.py ~/job-search/03-master-cv.pdf --claims claims.txt
    python3 scripts/verify_check.py

`make_tracker.py` writes an `.xlsx` with four tabs — applications, contacts,
interview history and a source summary with working attribution formulas — plus
CSVs for importing into Sheets, Notion or Airtable. Needs
`openpyxl`, or run `--csv-only` with no dependencies.

`ats_check.py` extracts the text back out of your CV the way an applicant
tracking system would, and tells you whether your section headings, contact
details and key claims survived — plus the structural things that break parsers:
tables, text boxes, two-column layouts, content stranded in headers. Uses
`pdftotext`, `pdfplumber` or `pypdf` for PDFs and `python-docx` for Word files,
whichever is present.

`verify_check.py` regression-tests the phase-7 verification protocol
(`references/10-verification.md`) — the rules that stop a live role being
reported dead. Run it after touching that file or the verdict logic it
encodes; it fails loudly rather than warning.

## Things it deliberately will not do

**Auto-submit applications.** The ceiling is drafted and staged; a human presses
submit. Applications cannot be un-sent, misconfigured filters fail in batches of
forty rather than one, and submission was never the bottleneck — fit, tailoring
and having someone inside are. `references/06-cadence-autonomy.md` makes the full
argument.

**Scrape LinkedIn or anything else that forbids it.** Alerts and saved searches do
the same job, legally, and the account that gets restricted is yours.

**Invent a fact about you.** Not a metric, not a date, not a team size. Unknowns
stay in the document as `[NEEDS NUMBER]` until you supply the answer. An invented
number is a fireable offence after you are hired.

**Tell you what to accept.** On packages, offers and legal questions it lays out
the numbers and the trade-offs. The decision is yours, and for real money you
should talk to a solicitor.

## Privacy

Your CV, salary and application history stay in your folder. This repository
contains no personal data, and `.gitignore` blocks `job-search/`, PDFs, Word files
and spreadsheets so you cannot commit yours by accident. If you fork this to
customise it, keep it that way.

## Accuracy

The Ireland figures in `references/09-ireland-redundancy.md` were verified in
August 2026 and every one carries a source link. Statutory ceilings and welfare
rates move with the Budget — check
[citizensinformation.ie](https://www.citizensinformation.ie),
[revenue.ie](https://www.revenue.ie) and
[workplacerelations.ie](https://www.workplacerelations.ie) before relying on any
number here. This is orientation, not legal, tax or financial advice.

## Contributing

Non-Irish equivalents of the entitlements module, local job-board coverage for
other cities, and better fit-scoring weights are all welcome. One rule: **no
personal data in examples, issues or pull requests.**

MIT licensed. Use it, fork it, pass it on to whoever needs it next.
