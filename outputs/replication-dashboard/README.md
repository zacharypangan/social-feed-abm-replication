# Replication Dashboard

Static dashboard for tracking Social Feed ABM replication progress, provenance,
and faithfulness.

Production: https://replication-dashboard.vercel.app

## Commands

```bash
npm run check
npm run dev
```

Docker:

```bash
docker build -t social-feed-abm-dashboard .
docker run --rm -p 4173:4173 social-feed-abm-dashboard
```

The dashboard uses sanitized summary data in `data/replication-data.json`; it
does not include raw ACL2017 or FakeNewsNet files.

## Current Views

- Concepts tab explaining the paper's SNA, diffusion, ABM, feed-curation,
  belief-purity, and calibration logic with animated visual summaries.
- Research Proposal tab explaining the exposure-aware semantic network
  simulation proposal, including framework layers, RQs, work packages,
  prototype scope, and contribution map.
- Phase and design-criteria status cards.
- Observed-vs-calibrated `Phi` curves.
- Actual-vs-paper curation intervention bars for Tables 4, 5, and B.2.
- Hub-focused synthetic agent-network snapshots with degree strips.
- Observed ACL2017 propagation cascade snapshots.
- Phase 6 target verdicts and provenance records.
