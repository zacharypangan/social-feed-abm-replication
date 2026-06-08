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
  const runCount = data.visual_summary?.phase5_simulation_run_count ?? 0;

  document.getElementById("overall-status").textContent = `${completePhases}/${data.phases.length} phases complete`;

  const cards = [
    ["Cases", caseCount, "Paper-relevant Twitter15 cascades"],
    ["Phases", `${completePhases}/${data.phases.length}`, "Implemented replication stages"],
    ["Criteria", `${criteriaComplete}/${data.faithfulness.length}`, "Paper design criteria satisfied"],
    ["Runs", runCount, "Phase 5 calibrated simulations"],
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

function renderPhiCharts(cases) {
  document.getElementById("phi-chart-grid").innerHTML = cases
    .map((item) => `
      <article class="chart-card">
        <div class="chart-card-head">
          <div>
            <span class="tag ${item.label === "false" ? "next" : "complete"}">${item.label}</span>
            <h3>${titleize(item.case_name)}</h3>
          </div>
          <p class="chart-stat">NRMSE ${formatNumber(item.calibration?.nrmse ?? 0, 3)}</p>
        </div>
        ${lineChart(item.calibration_series ?? [])}
        <div class="legend">
          <span><i class="legend-line observed"></i>Observed</span>
          <span><i class="legend-line predicted"></i>Calibrated</span>
        </div>
      </article>`)
    .join("");
}

function renderRelativeChanges(cases) {
  const rows = cases.flatMap((item) => item.feed_relative_changes ?? []);
  const maxAbs = Math.max(
    0.1,
    ...rows.flatMap((row) => [
      Math.abs(row.change_phi_avg),
      Math.abs(row.change_phi_max),
      Math.abs(row.change_belief_purity)
    ])
  );

  document.getElementById("relative-change-list").innerHTML = cases
    .map((item) => `
      <article class="comparison-card">
        <h3>${titleize(item.case_name)}</h3>
        ${(item.feed_relative_changes ?? [])
          .filter((row) => row.feed_algorithm !== "chronological")
          .map((row) => groupedBars(row, maxAbs))
          .join("")}
      </article>`)
    .join("");
}

function renderFakeNewsNetAudit(rows) {
  const totalArticles = rows.reduce((total, row) => total + row.article_count, 0);
  const totalTweetIds = rows.reduce((total, row) => total + row.tweet_id_count, 0);
  const maxTweetIds = Math.max(...rows.map((row) => row.tweet_id_count), 1);

  document.getElementById("fakenewsnet-audit-list").innerHTML = `
    <article class="audit-summary">
      <div><strong>${formatNumber(totalArticles, 0)}</strong><span>articles</span></div>
      <div><strong>${formatNumber(totalTweetIds, 0)}</strong><span>tweet IDs</span></div>
    </article>
    ${rows.map((row) => `
      <article class="audit-item">
        <div class="bar-label">
          <span>${titleize(`${row.source}_${row.label}`)}</span>
          <strong>${formatNumber(row.tweet_id_count, 0)}</strong>
        </div>
        <div class="bar-track">
          <div class="bar audit" style="width:${Math.max(3, (row.tweet_id_count / maxTweetIds) * 100)}%"></div>
        </div>
        <p class="case-meta">${formatNumber(row.article_count, 0)} articles, avg ${formatNumber(row.avg_tweet_ids_per_article, 1)} tweet IDs/article</p>
      </article>`)
      .join("")}`;
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
  const maxCalibrationNrmse = Math.max(
    0.25,
    ...cases.map((item) => item.calibration?.nrmse ?? 0)
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
            ${calibrationRows(item, maxCalibrationNrmse)}
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

function calibrationRows(item, maxCalibrationNrmse) {
  if (!item.calibration) return "";
  return `
    ${barRow("Calibration NRMSE", item.calibration.nrmse, maxCalibrationNrmse, "bar calibration")}
    <p class="case-meta">
      Best chronological fit: RMSE ${formatNumber(item.calibration.rmse, 5)},
      p_online ${formatNumber(item.calibration.p_online, 5)},
      p_reshare ${formatNumber(item.calibration.p_reshare, 5)}
    </p>`;
}

function lineChart(points) {
  if (!points.length) return `<div class="empty-chart">No curve data</div>`;
  const width = 420;
  const height = 180;
  const pad = 24;
  const maxTimestep = Math.max(...points.map((point) => point.timestep), 1);
  const maxPhi = Math.max(
    ...points.flatMap((point) => [point.observed_phi, point.predicted_phi]),
    0.001
  );
  const xFor = (timestep) => pad + (timestep / maxTimestep) * (width - pad * 2);
  const yFor = (phi) => height - pad - (phi / maxPhi) * (height - pad * 2);
  const pathFor = (key) => points
    .map((point, index) => `${index === 0 ? "M" : "L"} ${xFor(point.timestep).toFixed(2)} ${yFor(point[key]).toFixed(2)}`)
    .join(" ");
  const observedPoints = points
    .filter((_, index) => index % Math.max(1, Math.floor(points.length / 24)) === 0)
    .map((point) => `<circle cx="${xFor(point.timestep).toFixed(2)}" cy="${yFor(point.observed_phi).toFixed(2)}" r="2"></circle>`)
    .join("");

  return `
    <svg class="line-chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="Observed and calibrated Phi over time">
      <line class="axis" x1="${pad}" y1="${height - pad}" x2="${width - pad}" y2="${height - pad}"></line>
      <line class="axis" x1="${pad}" y1="${pad}" x2="${pad}" y2="${height - pad}"></line>
      <path class="chart-line observed" d="${pathFor("observed_phi")}"></path>
      <path class="chart-line predicted" d="${pathFor("predicted_phi")}"></path>
      <g class="chart-points">${observedPoints}</g>
    </svg>`;
}

function groupedBars(row, maxAbs) {
  const metrics = [
    ["Phi avg", row.change_phi_avg],
    ["Phi max", row.change_phi_max],
    ["Purity", row.change_belief_purity]
  ];
  return `
    <div class="comparison-row">
      <div class="comparison-label">${titleize(row.feed_algorithm)}</div>
      <div class="comparison-bars">
        ${metrics.map(([label, value]) => divergingBar(label, value, maxAbs)).join("")}
      </div>
    </div>`;
}

function divergingBar(label, value, maxAbs) {
  const width = Math.min(50, Math.abs(value / maxAbs) * 50);
  const style = value >= 0
    ? `left:50%;width:${width}%`
    : `left:${50 - width}%;width:${width}%`;
  return `
    <div class="diverging-row">
      <span>${label}</span>
      <div class="diverging-track">
        <i class="zero"></i>
        <i class="diverging-bar ${value >= 0 ? "positive" : "negative"}" style="${style}"></i>
      </div>
      <strong>${formatNumber(value, 3)}</strong>
    </div>`;
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
    renderPhiCharts(data.cases);
    renderRelativeChanges(data.cases);
    renderFakeNewsNetAudit(data.fakenewsnet_audit ?? []);
  })
  .catch((error) => {
    document.body.innerHTML = `<main><h1>Dashboard data error</h1><p>${error.message}</p></main>`;
  });
