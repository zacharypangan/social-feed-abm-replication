# Data Workflow

Use this guide to keep data handling reproducible, traceable, and safe.

## Data Areas

- `data/raw/`: immutable source data. Do not edit directly.
- `data/interim/`: temporary or partially processed files.
- `data/processed/`: reproducible cleaned/model-ready data.
- `data/external/`: third-party reference data.
- `outputs/`: generated predictions, reports, plots, logs, and exports.

Create subfolders only when the project needs them.

## Core Rules

- Never modify raw data directly; create a new processed output instead.
- Processed data should be reproducible from scripts plus configs.
- Document schemas, column meanings, units, labels, and expected types.
- Do not commit large files unless it is intentional and documented.
- Do not expose sensitive, private, licensed, or identifying data.
- Record data lineage from source to processed output.
- Keep restricted Twitter-derived cascade data local unless redistribution rights
  are explicit and documented.
- Prefer synthetic fixtures, schemas, acquisition notes, and processing
  instructions over committing raw social media data.
- If using the Ma et al. Twitter rumor dataset, document access constraints,
  acquisition date, selected story IDs/text labels, and preprocessing lineage.

## Data Lineage Checklist

- Source name, URL/path, owner, and license/usage constraints.
- Acquisition date and version/snapshot.
- Raw data path.
- Processing script and command.
- Config path and parameters.
- Output path.
- Row counts or record counts before and after processing.
- Filters, exclusions, joins, and label transformations.
- Known quality issues or missingness.

## Processing Script Expectations

- Accept explicit input and output paths.
- Avoid hidden working-directory assumptions.
- Validate schema before transformation.
- Write outputs without overwriting raw inputs.
- Log enough information to reproduce the run.

## Dataset Note Template

```text
Dataset:
Source:
License/constraints:
Acquired:
Version/snapshot:
Raw path:
Processed path:
Schema docs:
Processing command:
Lineage notes:
Known issues:
```
