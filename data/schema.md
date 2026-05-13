# Data Dictionary — WATCH-DM

> Fill in this table as variables are finalized. This file is **committed** to the repository (it does not contain PHI — only schema metadata).

## Identifiers

| Variable | Type | Description | Allowed values / units |
|----------|------|-------------|------------------------|
| `patient_id` | str | De-identified study ID (e.g. `WDM-0001`) | — |
| `enrollment_date` | date | Index date / first DM-related visit | ISO 8601 |

## Demographics

| Variable | Type | Description | Allowed values / units |
|----------|------|-------------|------------------------|
| `age` | int | Age at enrollment | years |
| `sex` | category | Biological sex | M / F |
| ... | | | |

## Clinical baseline

| Variable | Type | Description | Allowed values / units |
|----------|------|-------------|------------------------|
| `hba1c` | float | Glycated haemoglobin | % |
| `fbg` | float | Fasting blood glucose | mg/dL |
| `bmi` | float | Body mass index | kg/m² |
| `egfr` | float | Estimated GFR (CKD-EPI) | mL/min/1.73 m² |
| ... | | | |

## Comorbidities (binary 0/1)

| Variable | Type | Description |
|----------|------|-------------|
| `htn` | int | Hypertension |
| `dlp` | int | Dyslipidemia |
| `ckd` | int | Chronic kidney disease |
| ... | | |

## Outcomes / follow-up

| Variable | Type | Description | Allowed values / units |
|----------|------|-------------|------------------------|
| `event` | int | Primary event indicator | 0 = censored, 1 = event |
| `time_to_event` | float | Follow-up time | days |
| ... | | | |

---

*Last updated: 2026-05-13*
