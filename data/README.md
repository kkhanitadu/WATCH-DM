# Data — WATCH-DM

> **⚠️ Patient-level data are intentionally NOT included in this repository.**

## Why?

The WATCH-DM cohort contains protected health information (PHI). Sharing raw or even partially identifiable records on a public repository would violate:

- The Personal Data Protection Act (PDPA), Thailand
- The hospital's data-sharing agreement
- The study IRB approval

## What goes in this folder locally?

When you clone the repo, expect this folder to be **empty** apart from this README and the schema file. Place your local extract here (it will be ignored by git):

```
data/
├── README.md                  ← this file (committed)
├── schema.md                  ← data dictionary / column definitions (committed)
├── raw/                       ← original export (gitignored)
│   └── watch_dm_raw.parquet
├── interim/                   ← cleaned / typed (gitignored)
└── processed/                 ← analysis-ready (gitignored)
```

## How to request access

De-identified data may be available from the corresponding author upon reasonable request, subject to:

1. Signed data-sharing agreement
2. IRB approval at the requester's institution
3. Description of intended analyses

Contact: **kkhanita.du@up.ac.th**

## Schema

See [`schema.md`](schema.md) for the data dictionary (variable names, types, units, allowed values).
