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

## Observed Cascade Schema

Phase 2 reconstructs observed cascade events from ACL2017 propagation trees.
Generated outputs are written to `outputs/phase2_observed_cascades/` and remain
ignored by Git.

Per-case event rows include:

```text
story_id
case_name
label
source_tweet_id
parent_user_id
parent_tweet_id
user_id
tweet_id
delay_minutes
timestep
event_type
```

`event_type` is `source` for the `ROOT -> source` edge and `propagation` for all
non-root propagation edges. Phase 2 preserves source events in event tables but
excludes them from `Phi` by default.

Per-case `Phi` rows include:

```text
timestep
event_count
phi
```

The default binning is hourly: `timestep = floor(delay_minutes / 60)`. The
default denominator is `n_agents=1000`, matching the paper's ABM population as a
Phase 2 approximation.

## Phase 3 Simulation Trace Outputs

Phase 3 does not add new raw data requirements. It uses the same local ACL2017
case IDs for case selection and label checks, then runs a synthetic ABM with
paper-scale fixed parameters. Generated outputs are written to
`outputs/phase3_model_fidelity/simulations/` and remain ignored by Git.

Per-run JSON files include:

```text
phi_by_timestep
belief_purity_by_timestep
event_counts_by_timestep
state_counts_by_timestep
network_summary
```

The Phase 3 event trace records simulated `online`, `feed_view`,
`belief_update`, `reshare`, `reject`, `believe`, and `deny` counts per timestep.
These are simulated process records, not observed ACL2017 events.

## Phase 4 Calibration Outputs

Phase 4 reads the Phase 2 observed `Phi` targets and runs chronological
Phase 3-style simulations over a small probability grid. Generated outputs are
written to `outputs/phase4_calibration_validation/` and remain ignored by Git.

Top-level Phase 4 outputs include:

```text
candidate_scores.csv
candidate_scores.json
best_calibration_summary.csv
best_calibration_summary.json
manifest.json
```

Per-case folders include all candidate scores, run records, best-candidate
metadata, and observed-versus-predicted `Phi` rows for each candidate.

## Phase 5 Counterfactual Outputs

Phase 5 uses the three paper case studies, not the entire ACL2017 dataset, to
match the original study's case-study design. It applies each case's Phase 4
best chronological calibration to all four feed objectives and computes
paper-style relative changes against the chronological baseline.

Generated outputs are written to
`outputs/phase5_case_study_counterfactuals/` and remain ignored by Git.
FakeNewsNet is summarized only as a parameter-context audit using article-level
tweet-ID counts; it is not treated as a propagation-cascade validation target.

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
- Phase 2 reconstructs observed ACL2017 cascade events and padded `Phi` series
  for future chronological calibration and validation.
- Phase 3 adds simulated event/state traces and popularity-feedback mechanics
  while keeping the network synthetic and uncalibrated.
- Phase 4 calibrates chronological simulations against observed `Phi` targets
  using RMSE/NRMSE; the search is intentionally small and dependency-light.
- Phase 5 runs calibrated paper-style counterfactual comparisons and audits
  FakeNewsNet tweet-ID volume as context.
- External redistribution constraints remain unresolved.
