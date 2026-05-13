# Zenodo + GitHub Deployment Guide — Manual Upload

How to publish this repository to GitHub and obtain a citable DOI from Zenodo using **manual upload** (no GitHub–Zenodo automatic integration).

---

## Part A — Push to GitHub

```bash
cd WATCH-DM
git init -b main
git add .
git commit -m "Initial commit: scaffold WATCH-DM repository"

# Create empty repo at https://github.com/new (do NOT add README/LICENSE)
git remote add origin https://github.com/<your-username>/WATCH-DM.git
git push -u origin main
```

> Recommended repo settings on GitHub:
> - Visibility: **Public** (required if you want a free Zenodo DOI)
> - Description: "Data analysis pipeline for the WATCH-DM diabetes cohort study"
> - Topics: `diabetes`, `clinical-research`, `survival-analysis`, `reproducible-research`

---

## Part B — Manual Zenodo upload (each release)

### Step 1 — Tag the release on GitHub

```bash
# Update version in CITATION.cff first
git tag -a v0.1.0 -m "v0.1.0 — first public release"
git push origin v0.1.0
```

Then on GitHub: **Releases → Draft a new release → choose tag v0.1.0 → Publish release**.
GitHub will auto-generate `Source code (zip)` and `Source code (tar.gz)` files for download.

### Step 2 — Download the release ZIP

From the GitHub release page, right-click **Source code (zip)** → **Save As…**
Or via terminal:

```bash
curl -L -o WATCH-DM-v0.1.0.zip \
  https://github.com/<your-username>/WATCH-DM/archive/refs/tags/v0.1.0.zip
```

### Step 3 — Upload to Zenodo

1. Go to <https://zenodo.org/uploads/new>
2. **Files** — drag in `WATCH-DM-v0.1.0.zip`
3. **Basic information** — fill in using values from `.zenodo.json` (this repo includes that file as a reference for what to type):

   | Zenodo field | Value |
   |---|---|
   | Resource type | **Software** |
   | Title | `WATCH-DM: Data Analysis of Diabetes Mellitus Patients` |
   | Authors | Duangchaemkarn, Khanita — University of Phayao — *(add ORCID)* |
   | Description | (copy from `.zenodo.json` → `description`) |
   | License | **MIT License** |
   | Version | `v0.1.0` |
   | Keywords | diabetes mellitus, clinical data analysis, survival analysis, retrospective cohort, reproducible research, python |
   | Language | English |

4. **Related/alternate identifiers** — once the manuscript is accepted, add:
   - Relation: *is supplement to*
   - Identifier: the manuscript DOI

5. **Funding** — add grant numbers if applicable
6. Click **Save → Publish**

Zenodo will mint a DOI immediately (e.g. `10.5281/zenodo.XXXXXXX`).

### Step 4 — Add the DOI badge back to the repo

Edit `README.md` — replace `PLACEHOLDER` in the DOI badge with your real DOI:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

Commit and push:
```bash
git add README.md
git commit -m "docs: add Zenodo DOI badge for v0.1.0"
git push
```

---

## Subsequent releases — "New version" on Zenodo

For v0.2.0, v1.0.0, etc., **do not create a brand-new Zenodo deposit**. Instead:

1. On the existing Zenodo record → **New version**
2. Upload the new ZIP from the new GitHub release
3. Update the version number
4. Publish

This keeps all versions under the same **concept DOI** while each release gets its own **version DOI**.

> **Concept DOI** — use this in your manuscript (always points to latest version)
> **Version DOI** — cite a specific release (e.g. the exact version reviewers tested)

---

## What about `.zenodo.json`?

The `.zenodo.json` file in this repo is **only auto-consumed by the GitHub–Zenodo automatic integration**. With manual upload it serves as a **metadata reference** — copy values from it into the Zenodo web form when uploading. Keep it up to date so future-you (or co-authors) can copy-paste the right metadata.

---

## Versioning convention

Follow [Semantic Versioning](https://semver.org/):
- `v0.x.x` — pre-publication, breaking changes allowed
- `v1.0.0` — release coinciding with manuscript acceptance
- `v1.x.x` — post-publication patches / additional analyses

## Useful links

- Zenodo upload page: <https://zenodo.org/uploads/new>
- Citation File Format (CFF): <https://citation-file-format.github.io/>
- Semantic Versioning: <https://semver.org/>
