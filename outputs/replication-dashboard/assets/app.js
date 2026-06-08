const formatNumber = (value, digits = 4) =>
  Number(value).toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: value === 0 ? 0 : Math.min(2, digits)
  });

const titleize = (value) =>
  value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (char) => char.toUpperCase())
    .replace("Nonrumor", "Non-Rumor");

const statusClass = (status) => {
  if (status === "complete") return "complete";
  if (status === "next") return "next";
  return status === "partial" ? "partial" : "pending";
};

async function loadData() {
  const response = await fetch("data/replication-data.json");
  if (!response.ok) throw new Error("Could not load dashboard data");
  return response.json();
}

function renderSummary(data) {
  const completePhases = data.phases.filter((phase) => phase.status === "complete").length;
  const criteriaComplete = data.faithfulness.filter((item) => item.status === "complete").length;
  const caseCount = data.cases.length;
  const outputCount = data.provenance.outputs.length;

  document.getElementById("overall-status").textContent = `${completePhases}/${data.phases.length} phases complete`;

  const cards = [
    ["Cases", caseCount, "Paper-relevant Twitter15 cascades"],
    ["Phases", `${completePhases}/${data.phases.length}`, "Implemented replication stages"],
    ["Criteria", `${criteriaComplete}/${data.faithfulness.length}`, "Paper design criteria satisfied"],
    ["Outputs", outputCount, "Tracked dashboard provenance paths"]
  ];

  document.getElementById("summary-grid").innerHTML = cards
    .map(
      ([label, value, note]) => `
        <article class="metric-card">
          <p class="metric-label">${label}</p>
          <div class="metric-value">${value}</div>
          <p class="metric-note">${note}</p>
        </article>`
    )
    .join("");
}

function renderPhases(phases) {
  document.getElementById("phase-grid").innerHTML = phases
    .map(
      (phase) => `
        <article class="phase-card">
          <span class="tag ${statusClass(phase.status)}">${phase.status}</span>
          <h3>${phase.name}</h3>
          <p class="phase-meta">${phase.description}</p>
          <p class="phase-meta"><strong>Evidence:</strong> ${phase.evidence}</p>
        </article>`
    )
    .join("");
}

function renderFaithfulness(criteria) {
  document.getElementById("criteria-list").innerHTML = criteria
    .map(
      (item) => `
        <article class="criterion">
          <span class="dot ${statusClass(item.status)}"></span>
          <div>
            <h3>${item.name}</h3>
            <p>${item.assessment}</p>
          </div>
        </article>`
    )
    .join("");
}

function renderProvenance(provenance) {
  const items = [
    ...provenance.inputs.map((input) => ({
      title: input.name,
      body: `${input.role} Path: ${input.path}`
    })),
    ...provenance.outputs.map((output) => ({
      title: output.name,
      body: `${output.role} Path: ${output.path}`
    }))
  ];

  document.getElementById("provenance-list").innerHTML = items
    .map(
      (item) => `
        <article class="provenance-item">
          <h3>${item.title}</h3>
          <p>${item.body}</p>
        </article>`
    )
    .join("");
}

function renderCases(cases) {
  const maxObservedPhi = Math.max(...cases.map((item) => item.observed.observed_phi_max));
  const maxSimPhi = Math.max(
    ...cases.flatMap((item) => item.simulated_feeds.map((feed) => feed.phi_max_mean))
  );

  document.getElementById("case-grid").innerHTML = cases
    .map((item) => {
      const rows = item.simulated_feeds
        .map(
          (feed) => `
            <tr>
              <td>${titleize(feed.feed_algorithm)}</td>
              <td>${formatNumber(feed.phi_avg_mean, 5)}</td>
              <td>${formatNumber(feed.phi_max_mean, 5)}</td>
              <td>${formatNumber(feed.belief_purity_avg_mean, 3)}</td>
              <td>${formatNumber(feed.reshare_events_mean ?? 0, 1)}</td>
              <td>${formatNumber(feed.deny_events_mean ?? 0, 1)}</td>
            </tr>`
        )
        .join("");

      const topFeed = item.simulated_feeds.reduce((best, feed) =>
        feed.phi_max_mean > best.phi_max_mean ? feed : best
      );

      return `
        <article class="case-card">
          <span class="tag ${item.label === "false" ? "next" : "complete"}">${item.label}</span>
          <h3>${titleize(item.case_name)}</h3>
          <p class="case-meta">Story ID ${item.story_id}</p>
          <div class="bar-list">
            ${barRow("Observed Phi max", item.observed.observed_phi_max, maxObservedPhi, "bar")}
            ${barRow("Observed Phi avg", item.observed.observed_phi_avg, maxObservedPhi, "bar")}
            ${barRow(`Simulation top Phi max (${titleize(topFeed.feed_algorithm)})`, topFeed.phi_max_mean, maxSimPhi, "bar sim")}
            ${barRow("Belief-feed purity", beliefPurityFor(item), 1, "bar purity")}
          </div>
          <table class="case-table">
            <thead>
              <tr><th>Feed</th><th>Phi avg</th><th>Phi max</th><th>Purity</th><th>Reshare</th><th>Deny</th></tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </article>`;
    })
    .join("");
}

function beliefPurityFor(item) {
  const belief = item.simulated_feeds.find((feed) => feed.feed_algorithm === "belief");
  return belief ? belief.belief_purity_avg_mean : 0;
}

function barRow(label, value, max, className) {
  const width = max > 0 ? Math.max(3, (value / max) * 100) : 0;
  return `
    <div class="bar-row">
      <div class="bar-label"><span>${label}</span><strong>${formatNumber(value, 4)}</strong></div>
      <div class="bar-track"><div class="${className}" style="width:${width}%"></div></div>
    </div>`;
}

loadData()
  .then((data) => {
    renderSummary(data);
    renderPhases(data.phases);
    renderFaithfulness(data.faithfulness);
    renderProvenance(data.provenance);
    renderCases(data.cases);
  })
  .catch((error) => {
    document.body.innerHTML = `<main><h1>Dashboard data error</h1><p>${error.message}</p></main>`;
  });
