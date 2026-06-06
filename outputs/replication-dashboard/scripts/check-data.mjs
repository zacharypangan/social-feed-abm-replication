import { readFileSync } from "node:fs";

const data = JSON.parse(readFileSync("data/replication-data.json", "utf8"));
const requiredTopLevel = ["project", "phases", "cases", "faithfulness", "provenance"];
const missing = requiredTopLevel.filter((key) => !(key in data));

if (missing.length) {
  throw new Error(`Missing dashboard data keys: ${missing.join(", ")}`);
}

if (!Array.isArray(data.cases) || data.cases.length === 0) {
  throw new Error("Dashboard data must include at least one case.");
}

console.log(`Dashboard data OK: ${data.cases.length} cases, ${data.phases.length} phases.`);
