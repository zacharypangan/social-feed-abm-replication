# Experiment Tracking

Use this guide to make experiment runs reproducible and comparable.

## Track For Every Run

- Config path and saved config contents.
- Seed and any nondeterministic behavior.
- Parameters that affect data, model, prompts, training, inference, or evaluation.
- Metrics and how they are computed.
- Output folder.
- Logs.
- Model checkpoints or external model identifiers.
- Result tables and figure paths.
- Exact command used to reproduce the run.

## Suggested Output Layout

```text
outputs/
  {run_id}/
    config.*
    command.txt
    metrics.*
    results.*
    logs/
    checkpoints/
    figures/
```

Use only the folders the project actually needs.

## Minimum Run Record

```text
Run ID:
Date:
Question:
Code version:
Command:
Config path:
Seed:
Parameters:
Input data path/version:
Model/checkpoint:
Metrics:
Output folder:
Logs:
Result tables:
Notes:
```

## Reproduce A Run

1. Checkout the recorded code version if available.
2. Confirm data path/version and schema.
3. Use the saved config and parameters.
4. Run the recorded command.
5. Compare metrics, logs, result tables, and output files.
6. Record any nondeterministic differences.

## LLM Experiment Notes

- Record provider, model name, and model version/date when available.
- Record prompt template, system instructions, and decoding parameters.
- Record evaluation method and judge model if used.
- Avoid storing sensitive prompts, private data, or raw responses unless approved.

## Comparison Table

| Run ID | Config | Seed | Data | Metric | Output | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | TODO | TODO | TODO | TODO |
