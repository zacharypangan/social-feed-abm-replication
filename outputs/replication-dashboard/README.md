# Replication Dashboard

Static dashboard for tracking Social Feed ABM replication progress, provenance,
and faithfulness.

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
