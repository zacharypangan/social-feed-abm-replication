# Data Documentation

This directory documents data used by the Social Feed ABM Replication project.
No raw restricted Twitter-derived cascade data should be committed here unless
redistribution rights are explicit and documented.

## Data Policy

- Start with synthetic data and schema fixtures before using external cascade
  data.
- Keep raw data immutable. Do not edit files under `data/raw/` directly.
- Do not commit private, sensitive, personally identifying, licensed, or
  redistribution-restricted social media data.
- Prefer public instructions, schemas, synthetic samples, and processing notes
  over raw Twitter-derived files.
- Record lineage for every processed dataset used in a result.

## Planned Data Areas

Create these folders only when needed:

```text
data/
  raw/          # Local immutable source files, usually not committed.
  interim/      # Temporary intermediate files from processing.
  processed/    # Reproducible model-ready datasets.
  synthetic/    # Synthetic fixtures and small generated examples.
  external/     # Third-party reference files with documented licenses.
```

Generated results, metrics, plots, and logs should go under `outputs/`, not
`data/`.

## Expected Data Sources

### Synthetic Replication Data

- Purpose: support the first ABM smoke workflow without external data access.
- Expected contents: generated networks, synthetic story events, initial agent
  states, and small fixtures for tests.
- Commit policy: small synthetic fixtures may be committed if they are clearly
  documented and reproducible.

### Historical Twitter Cascade Data

- Candidate source: Ma et al. Twitter rumor cascade dataset referenced by the
  original study.
- Purpose: calibrate and validate the chronological-feed baseline against
  historical cascades when obtainable.
- Commit policy: do not commit raw cascade data unless redistribution rights are
  explicit and documented.
- Required notes: source, access method, license/usage constraints, acquisition
  date, selected story/case labels, schema, preprocessing command, and lineage.

Local Phase 1 notes:

- `data/rumor_detection_acl2017/` is expected locally for the data-assisted MVP.
- The selected Twitter15 source-tweet IDs are `505369323922522113`
  (false/Tupac), `692812029611089920` (non-rumor/Justin Bieber), and
  `553960736964476928` (false/Helric Fredou).
- `data/FakeNewsNet dataset/` is available locally as a later extension source,
  but it is not used by the Phase 1 MVP.
- Both raw dataset folders should remain ignored by Git.

## Planned Cascade Schema

The exact schema will be finalized during data preprocessing. Expected fields
for processed cascade records include:

```text
story_id
story_label
is_false_or_rumor
post_id
user_id
parent_post_id
timestamp
timestep
event_type
retweet_count
follower_count
source_dataset
```

Network or user-level processed data may additionally include:

```text
user_id
followee_id
follower_id
degree
verified
initial_belief
initial_state
```

## Lineage Record Template

Use this template for each real or synthetic dataset:

```text
Dataset:
Purpose:
Source:
License/constraints:
Acquired/generated:
Version/snapshot:
Raw path:
Processed path:
Schema:
Processing command:
Rows/records before:
Rows/records after:
Filters/exclusions:
Known issues:
Notes:
```

## Current Status

- Local ACL2017 and FakeNewsNet files are present for exploration and Phase 1
  planning, but raw files are not intended for GitHub.
- Phase 1 uses ACL2017 Twitter15 case summaries and synthetic counterfactual
  simulation outputs.
- External redistribution constraints remain unresolved.
