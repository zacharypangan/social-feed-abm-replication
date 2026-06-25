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
  if (status === "complete" || status === "matched") return "complete";
  if (status === "next" || status === "directionally_matched") return "next";
  return status === "partial" || status === "blocked" ? "partial" : "pending";
};

const conceptCards = [
  {
    label: "SNA",
    title: "Social Network Analysis",
    body: "Users are represented as agents connected by follower and followee ties. The network shape matters because hubs can expose many agents to the same story.",
    signal: "Nodes, ties, hubs",
    tone: "sna"
  },
  {
    label: "Diffusion",
    title: "Information Diffusion",
    body: "A story spreads when agents post, reshare, deny, or stop engaging with it over time. The dashboard summarizes spread with per-timestep story activity.",
    signal: "Phi over time",
    tone: "diffusion"
  },
  {
    label: "ABM",
    title: "Agent-Based Model",
    body: "The paper uses simulated users with states, beliefs, and probabilities for going online, viewing feeds, and reacting to posts.",
    signal: "Agents + rules",
    tone: "abm"
  },
  {
    label: "Feeds",
    title: "Algorithmic Curation",
    body: "The central intervention is the feed objective: chronological, belief-based, popularity-based, or random ranking of candidate posts.",
    signal: "Ranking rule",
    tone: "curation"
  },
  {
    label: "Belief",
    title: "Belief Purity",
    body: "Belief purity approximates how similar viewed feed content is to an agent's own belief, making feed homogeneity and echo-chamber risk measurable.",
    signal: "Content similarity",
    tone: "belief"
  },
  {
    label: "Fit",
    title: "Calibration And Validation",
    body: "A chronological baseline is fit to observed cascade traces, then the same case is rerun under alternative feed objectives for comparison.",
    signal: "RMSE, NRMSE",
    tone: "fit"
  }
];

const feedObjectives = [
  ["Chronological", "Newest candidate posts first", "Baseline behavior to calibrate before interventions"],
  ["Popularity", "Posts with more retweets, followers, and recency first", "Tests whether popularity amplification increases spread"],
  ["Belief", "Posts closest to the viewing agent's belief first", "Tests whether similarity-based curation increases purity"],
  ["Random", "Candidate posts shuffled before viewing", "A comparison condition that removes directed ranking pressure"]
];

const paperQuestionPaths = [
  {
    question: "Can false and non-false diffusion be modeled?",
    method: "Use rumor and non-rumor case studies, then track story-related posting over time.",
    evidence: "Observed cascade traces and simulated Phi curves"
  },
  {
    question: "Can the model represent a Twitter-like social system?",
    method: "Place agents on a follower/followee network with hub structure and local feed visibility.",
    evidence: "Synthetic Barabasi-Albert agent network snapshots"
  },
  {
    question: "Can real cascade data calibrate and validate the model?",
    method: "Fit the chronological baseline to observed propagation targets before comparing interventions.",
    evidence: "RMSE and NRMSE validation records"
  },
  {
    question: "Can beliefs and echo-chamber tendencies be measured?",
    method: "Give agents scalar beliefs, update them from viewed content, and summarize feed homogeneity.",
    evidence: "Belief purity and state-transition summaries"
  },
  {
    question: "What changes when feed objectives change?",
    method: "Reuse calibrated case settings across chronological, popularity, belief, and random feeds.",
    evidence: "Relative changes in Phi avg, Phi max, and belief purity"
  }
];

const proposalLayers = [
  {
    label: "Language",
    title: "Content And Meaning",
    body: "Posts, claims, topics, stance, sentiment, toxicity, uncertainty, and source cues become structured semantic features.",
    examples: "claims, topics, stance"
  },
  {
    label: "Actors",
    title: "Users And Sources",
    body: "Users, public accounts, media sources, fact-checkers, communities, and moderation actors are represented as entities.",
    examples: "users, sources, communities"
  },
  {
    label: "Network",
    title: "Relations And Diffusion Paths",
    body: "Follows, replies, reposts, mentions, citations, co-hashtag use, and communities define the paths where diffusion can occur.",
    examples: "edges, hubs, communities"
  },
  {
    label: "Exposure",
    title: "What Users Could See",
    body: "Observed, inferred, simulated, and counterfactual exposure records make feed ranking part of the model instead of an invisible assumption.",
    examples: "observed, inferred, simulated"
  },
  {
    label: "Intervention",
    title: "Platform Actions",
    body: "Fact-check labels, downranking, reranking, friction prompts, source diversification, and moderation become testable counterfactuals.",
    examples: "labels, reranking, friction"
  },
  {
    label: "Governance",
    title: "Reproducibility Under Constraints",
    body: "Provenance, access conditions, deletion status, datasheets, model cards, and shareability rules keep constrained data scientifically traceable.",
    examples: "provenance, datasheets"
  }
];

const proposalRqs = [
  ["RQ1", "Semantic Representation", "How can content, actors, claims, topics, sources, exposure, interventions, and provenance fit into one semantic network?"],
  ["RQ2", "Exposure Modeling", "How can feed exposure be represented when ranking logs are unavailable, partial, inferred, or simulated?"],
  ["RQ3", "Diffusion Modeling", "How do graph models, knowledge graphs, and LLM-agent simulations differ in reproducing diffusion patterns?"],
  ["RQ4", "Simulation Fidelity", "Which metrics show whether a simulation matches network, language, cascade, exposure, and intervention behavior?"],
  ["RQ5", "Counterfactual Intervention", "How can simulations evaluate fact-checking, moderation, downranking, reranking, diversification, or friction prompts?"],
  ["RQ6", "Governance-Aware Reproducibility", "How can benchmarks remain reusable while respecting platform terms, deletion requirements, privacy, and access limits?"]
];

const proposalWorkPackages = [
  ["WP1", "Semantic-network benchmark schema", "Define entities, edges, metadata, and export formats."],
  ["WP2", "Pilot benchmark construction", "Build a public, synthetic, or semi-synthetic testbed with provenance."],
  ["WP3", "Exposure-aware diffusion models", "Compare text-only, graph-only, temporal, KG, GNN, LLM-agent, and hybrid baselines."],
  ["WP4", "LLM-agent simulation and calibration", "Condition agents on graph position, exposure history, source trust, stance, and style."],
  ["WP5", "Simulation fidelity evaluation", "Measure network, cascade, linguistic, exposure, intervention, and robustness fidelity."],
  ["WP6", "Counterfactual interventions", "Test labels, downranking, source diversification, bridge exposure, and friction."],
  ["WP7", "Governance-aware reproducibility", "Track provenance, deletion status, versions, datasheets, model cards, and cleanroom workflows."]
];

const proposalPrototypeSteps = [
  "Load a small public or synthetic social media-like dataset.",
  "Represent users, posts, topics, claims, and interactions as a graph.",
  "Infer exposure from network neighbors, timestamps, and activity windows.",
  "Run text, graph, and simple diffusion baselines.",
  "Simulate graph-conditioned agents with predefined profiles.",
  "Compare observed and simulated cascade, topic, stance, and exposure behavior.",
  "Run one intervention such as fact-checking, downranking, or source diversification.",
  "Generate a provenance-rich reproducibility report."
];

const proposalContributions = [
  ["Theoretical", "Frames diffusion as an exposure-aware semantic network process."],
  ["Methodological", "Unifies NLP, SNA, GNNs, recommender modeling, and ABM validation."],
  ["Technical", "Provides reusable schema, exposure modeling, simulation, and fidelity tools."],
  ["Empirical", "Supports case studies on misinformation, echo chambers, or public discourse under data scarcity."],
  ["Governance", "Builds reproducible workflows for restricted, deletion-aware, platform-constrained data."]
];

async function loadData() {
  const response = await fetch("data/replication-data.json");
  if (!response.ok) throw new Error("Could not load dashboard data");
  return response.json();
}

function setupTabs() {
  const buttons = [...document.querySelectorAll(".tab-button")];
  const panels = [...document.querySelectorAll(".tab-panel")];
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.dataset.tabTarget;
      buttons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("active", active);
        item.setAttribute("aria-selected", String(active));
      });
      panels.forEach((panel) => {
        const active = panel.id === targetId;
        panel.classList.toggle("active", active);
        panel.hidden = !active;
      });
    });
  });
}

function renderConcepts() {
  const conceptGrid = document.getElementById("concept-card-grid");
  if (!conceptGrid) return;

  document.getElementById("concept-map-visual").innerHTML = conceptMapSvg();
  document.getElementById("abm-loop-visual").innerHTML = abmLoopSvg();

  conceptGrid.innerHTML = conceptCards
    .map((item) => `
      <article class="concept-card ${item.tone}">
        <div class="concept-card-head">
          <span class="concept-token">${item.label}</span>
          <strong>${item.signal}</strong>
        </div>
        <div class="concept-animation" aria-hidden="true">
          ${conceptAnimationSvg(item.tone)}
        </div>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
      </article>`)
    .join("");

  document.getElementById("feed-objective-list").innerHTML = feedObjectives
    .map(([name, rule, role]) => `
      <article class="feed-objective">
        <div>
          <h3>${name}</h3>
          <p>${rule}</p>
        </div>
        <strong>${role}</strong>
      </article>`)
    .join("");

  document.getElementById("paper-rq-list").innerHTML = paperQuestionPaths
    .map((item, index) => `
      <article class="rq-card">
        <div class="rq-number">${index + 1}</div>
        <div>
          <h3>${item.question}</h3>
          <p>${item.method}</p>
          <strong>${item.evidence}</strong>
        </div>
      </article>`)
    .join("");
}

function renderProposal() {
  const layerGrid = document.getElementById("proposal-layer-grid");
  if (!layerGrid) return;

  document.getElementById("proposal-map-visual").innerHTML = proposalMapSvg();
  document.getElementById("proposal-prototype-visual").innerHTML = proposalPrototypeSvg();

  layerGrid.innerHTML = proposalLayers
    .map((item) => `
      <article class="proposal-layer-card">
        <span class="proposal-token">${item.label}</span>
        <h3>${item.title}</h3>
        <p>${item.body}</p>
        <strong>${item.examples}</strong>
      </article>`)
    .join("");

  document.getElementById("proposal-rq-grid").innerHTML = proposalRqs
    .map(([label, title, body]) => `
      <article class="proposal-rq-card">
        <span>${label}</span>
        <h3>${title}</h3>
        <p>${body}</p>
      </article>`)
    .join("");

  document.getElementById("proposal-work-list").innerHTML = proposalWorkPackages
    .map(([label, title, body]) => `
      <article class="proposal-work-item">
        <span>${label}</span>
        <div>
          <h3>${title}</h3>
          <p>${body}</p>
        </div>
      </article>`)
    .join("");

  document.getElementById("proposal-prototype-list").innerHTML = proposalPrototypeSteps
    .map((step, index) => `
      <article>
        <span>${index + 1}</span>
        <p>${step}</p>
      </article>`)
    .join("");

  document.getElementById("proposal-contribution-grid").innerHTML = proposalContributions
    .map(([title, body]) => `
      <article class="proposal-contribution-card">
        <h3>${title}</h3>
        <p>${body}</p>
      </article>`)
    .join("");
}

function proposalMapSvg() {
  return `
    <svg class="proposal-svg" viewBox="0 0 760 410" role="img" aria-label="Exposure-aware semantic network proposal map">
      <defs>
        <marker id="proposal-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z"></path>
        </marker>
      </defs>
      <g class="proposal-orbit">
        <ellipse cx="380" cy="204" rx="238" ry="132"></ellipse>
        <ellipse cx="380" cy="204" rx="170" ry="88"></ellipse>
      </g>
      ${proposalLayerNode(120, 108, "Language", "posts, claims")}
      ${proposalLayerNode(324, 72, "Actors", "users, sources")}
      ${proposalLayerNode(560, 108, "Network", "ties, communities")}
      ${proposalLayerNode(598, 288, "Exposure", "feeds, ranking")}
      ${proposalLayerNode(326, 336, "Intervention", "rerank, labels")}
      ${proposalLayerNode(116, 288, "Governance", "provenance")}
      <path class="proposal-flow f1" d="M 188 112 C 270 128 310 164 360 190" marker-end="url(#proposal-arrow)"></path>
      <path class="proposal-flow f2" d="M 394 108 C 414 142 414 166 396 190" marker-end="url(#proposal-arrow)"></path>
      <path class="proposal-flow f3" d="M 532 138 C 490 154 446 174 404 194" marker-end="url(#proposal-arrow)"></path>
      <path class="proposal-flow f4" d="M 554 284 C 500 254 452 232 410 214" marker-end="url(#proposal-arrow)"></path>
      <path class="proposal-flow f5" d="M 388 310 C 388 276 388 248 388 226" marker-end="url(#proposal-arrow)"></path>
      <path class="proposal-flow f6" d="M 178 280 C 240 250 302 226 350 212" marker-end="url(#proposal-arrow)"></path>
      <g class="proposal-core">
        <circle cx="380" cy="204" r="58"></circle>
        <text x="380" y="194">
          <tspan x="380">Semantic</tspan>
          <tspan x="380" dy="18">network</tspan>
          <tspan x="380" dy="18">benchmark</tspan>
        </text>
      </g>
      <g class="proposal-pulse">
        <circle cx="380" cy="204" r="10"></circle>
        <circle cx="380" cy="204" r="10"></circle>
      </g>
    </svg>`;
}

function proposalLayerNode(x, y, title, note) {
  return `
    <g class="proposal-node" transform="translate(${x - 72} ${y - 38})">
      <rect width="144" height="76" rx="8"></rect>
      <text x="72" y="30">
        <tspan class="node-title" x="72">${title}</tspan>
        <tspan x="72" dy="20">${note}</tspan>
      </text>
    </g>`;
}

function proposalPrototypeSvg() {
  return `
    <svg class="proposal-prototype-svg" viewBox="0 0 520 260" role="img" aria-label="Minimal prototype pipeline">
      <defs>
        <marker id="prototype-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z"></path>
        </marker>
      </defs>
      <path class="prototype-link" d="M 124 72 H 218" marker-end="url(#prototype-arrow)"></path>
      <path class="prototype-link" d="M 302 72 H 396" marker-end="url(#prototype-arrow)"></path>
      <path class="prototype-link" d="M 438 106 C 438 140 380 150 340 150" marker-end="url(#prototype-arrow)"></path>
      <path class="prototype-link" d="M 218 150 H 124" marker-end="url(#prototype-arrow)"></path>
      ${prototypeNode(76, 72, "Data", "public/synthetic")}
      ${prototypeNode(260, 72, "Graph", "semantic network")}
      ${prototypeNode(444, 72, "Exposure", "inferred feeds")}
      ${prototypeNode(260, 150, "Simulate", "agents + baselines")}
      ${prototypeNode(76, 150, "Evaluate", "fidelity metrics")}
      <g class="prototype-report">
        <rect x="334" y="194" width="124" height="40" rx="8"></rect>
        <text x="396" y="219">Report</text>
      </g>
      <path class="prototype-link report" d="M 124 174 C 180 218 260 218 330 214" marker-end="url(#prototype-arrow)"></path>
      <circle class="prototype-runner" cx="76" cy="72" r="6"></circle>
    </svg>`;
}

function prototypeNode(x, y, title, note) {
  return `
    <g class="prototype-node" transform="translate(${x - 54} ${y - 34})">
      <rect width="108" height="68" rx="8"></rect>
      <text x="54" y="28">
        <tspan class="node-title" x="54">${title}</tspan>
        <tspan x="54" dy="18">${note}</tspan>
      </text>
    </g>`;
}

function conceptAnimationSvg(tone) {
  if (tone === "sna") return snaMiniViz();
  if (tone === "diffusion") return diffusionMiniViz();
  if (tone === "abm") return abmMiniViz();
  if (tone === "curation") return curationMiniViz();
  if (tone === "belief") return beliefMiniViz();
  return fitMiniViz();
}

function snaMiniViz() {
  return `
    <svg class="mini-viz sna-viz" viewBox="0 0 360 150" role="img" aria-label="Animated hub network">
      <g class="mini-ties">
        <line x1="178" y1="74" x2="78" y2="40"></line>
        <line x1="178" y1="74" x2="92" y2="106"></line>
        <line x1="178" y1="74" x2="278" y2="34"></line>
        <line x1="178" y1="74" x2="286" y2="106"></line>
        <line x1="78" y1="40" x2="92" y2="106"></line>
        <line x1="278" y1="34" x2="286" y2="106"></line>
      </g>
      <circle class="hub-ring" cx="178" cy="74" r="24"></circle>
      <g class="mini-packets">
        <circle class="packet p1" cx="178" cy="74" r="4"></circle>
        <circle class="packet p2" cx="178" cy="74" r="4"></circle>
        <circle class="packet p3" cx="178" cy="74" r="4"></circle>
      </g>
      <circle class="mini-node hub" cx="178" cy="74" r="13"></circle>
      <circle class="mini-node" cx="78" cy="40" r="8"></circle>
      <circle class="mini-node" cx="92" cy="106" r="8"></circle>
      <circle class="mini-node" cx="278" cy="34" r="8"></circle>
      <circle class="mini-node" cx="286" cy="106" r="8"></circle>
      <circle class="mini-node leaf" cx="214" cy="118" r="6"></circle>
    </svg>`;
}

function diffusionMiniViz() {
  return `
    <svg class="mini-viz diffusion-viz" viewBox="0 0 360 150" role="img" aria-label="Animated diffusion cascade">
      <path class="diffusion-path" d="M 44 98 C 90 60 124 54 168 72 S 250 110 318 42"></path>
      <g>
        <circle class="spread-dot d1" cx="44" cy="98" r="8"></circle>
        <circle class="spread-dot d2" cx="104" cy="64" r="7"></circle>
        <circle class="spread-dot d3" cx="168" cy="72" r="7"></circle>
        <circle class="spread-dot d4" cx="236" cy="102" r="7"></circle>
        <circle class="spread-dot d5" cx="318" cy="42" r="7"></circle>
      </g>
      <g class="phi-bars">
        <rect class="phi-bar b1" x="50" y="120" width="18" height="12" rx="3"></rect>
        <rect class="phi-bar b2" x="86" y="110" width="18" height="22" rx="3"></rect>
        <rect class="phi-bar b3" x="122" y="100" width="18" height="32" rx="3"></rect>
        <rect class="phi-bar b4" x="158" y="88" width="18" height="44" rx="3"></rect>
        <rect class="phi-bar b5" x="194" y="104" width="18" height="28" rx="3"></rect>
        <rect class="phi-bar b6" x="230" y="94" width="18" height="38" rx="3"></rect>
      </g>
    </svg>`;
}

function abmMiniViz() {
  return `
    <svg class="mini-viz abm-viz" viewBox="0 0 360 150" role="img" aria-label="Animated agent decision loop">
      <path class="loop-track" d="M 96 42 H 250 Q 282 42 282 74 V 76 Q 282 108 250 108 H 96 Q 64 108 64 76 V 74 Q 64 42 96 42"></path>
      ${abmStepGroup(88, 42, "Agents", "s1")}
      ${abmStepGroup(254, 42, "Feed", "s2")}
      ${abmStepGroup(254, 108, "React", "s3")}
      ${abmStepGroup(88, 108, "Record", "s4")}
      <circle class="agent-token" cx="88" cy="42" r="6"></circle>
      <g class="state-dots">
        <circle class="state-dot believe" cx="156" cy="75" r="7"></circle>
        <circle class="state-dot deny" cx="180" cy="75" r="7"></circle>
        <circle class="state-dot cured" cx="204" cy="75" r="7"></circle>
      </g>
    </svg>`;
}

function abmStepGroup(x, y, label, className) {
  return `
    <g class="abm-step ${className}" transform="translate(${x - 38} ${y - 19})">
      <rect width="76" height="38" rx="8"></rect>
      <text x="38" y="24">${label}</text>
    </g>`;
}

function curationMiniViz() {
  return `
    <svg class="mini-viz curation-viz" viewBox="0 0 360 150" role="img" aria-label="Animated ranked feed cards">
      <g class="ranking-lane">
        <line x1="58" y1="32" x2="58" y2="118"></line>
        <line x1="302" y1="32" x2="302" y2="118"></line>
      </g>
      <g class="post-stack source">
        <rect x="34" y="28" width="112" height="24" rx="6"></rect>
        <rect x="34" y="64" width="112" height="24" rx="6"></rect>
        <rect x="34" y="100" width="112" height="24" rx="6"></rect>
      </g>
      <g class="post-stack ranked">
        <rect class="rank-card r1" x="214" y="28" width="112" height="24" rx="6"></rect>
        <rect class="rank-card r2" x="214" y="64" width="112" height="24" rx="6"></rect>
        <rect class="rank-card r3" x="214" y="100" width="112" height="24" rx="6"></rect>
      </g>
      <path class="rank-arrow a1" d="M 150 40 C 178 40 188 40 210 40"></path>
      <path class="rank-arrow a2" d="M 150 76 C 178 64 188 52 210 40"></path>
      <path class="rank-arrow a3" d="M 150 112 C 178 112 188 112 210 112"></path>
      <rect class="feed-window" x="206" y="20" width="128" height="112" rx="10"></rect>
    </svg>`;
}

function beliefMiniViz() {
  return `
    <svg class="mini-viz belief-viz" viewBox="0 0 360 150" role="img" aria-label="Animated belief similarity alignment">
      <line class="belief-axis" x1="44" y1="96" x2="316" y2="96"></line>
      <rect class="belief-band" x="214" y="58" width="78" height="74" rx="10"></rect>
      <circle class="belief-agent" cx="252" cy="96" r="11"></circle>
      <circle class="belief-dot bd1" cx="86" cy="96" r="7"></circle>
      <circle class="belief-dot bd2" cx="128" cy="96" r="7"></circle>
      <circle class="belief-dot bd3" cx="178" cy="96" r="7"></circle>
      <circle class="belief-dot bd4" cx="300" cy="96" r="7"></circle>
      <path class="purity-arc" d="M 86 58 C 140 34 214 34 252 58"></path>
      <path class="purity-arc reverse" d="M 300 58 C 282 44 264 44 252 58"></path>
    </svg>`;
}

function fitMiniViz() {
  return `
    <svg class="mini-viz fit-viz" viewBox="0 0 360 150" role="img" aria-label="Animated observed and predicted fit curves">
      <line class="fit-axis" x1="42" y1="116" x2="318" y2="116"></line>
      <line class="fit-axis" x1="42" y1="28" x2="42" y2="116"></line>
      <path class="fit-line observed-fit" pathLength="1" d="M 44 96 L 88 62 L 132 86 L 176 48 L 220 74 L 264 58 L 314 88"></path>
      <path class="fit-line predicted-fit" pathLength="1" d="M 44 100 L 88 70 L 132 82 L 176 62 L 220 78 L 264 68 L 314 82"></path>
      <g class="residual-bars">
        <line class="residual r1" x1="88" y1="62" x2="88" y2="70"></line>
        <line class="residual r2" x1="176" y1="48" x2="176" y2="62"></line>
        <line class="residual r3" x1="264" y1="58" x2="264" y2="68"></line>
      </g>
    </svg>`;
}

function conceptMapSvg() {
  return `
    <svg class="concept-svg" viewBox="0 0 760 390" role="img" aria-label="Concept map linking social network analysis, ABM, feed curation, diffusion, and validation">
      <defs>
        <marker id="concept-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z"></path>
        </marker>
      </defs>
      <path class="concept-link" d="M 190 105 C 255 65 315 65 380 105" marker-end="url(#concept-arrow)"></path>
      <path class="concept-link" d="M 470 105 C 535 65 595 65 660 105" marker-end="url(#concept-arrow)"></path>
      <path class="concept-link" d="M 660 175 C 615 245 555 275 470 280" marker-end="url(#concept-arrow)"></path>
      <path class="concept-link" d="M 380 280 C 300 280 235 245 190 175" marker-end="url(#concept-arrow)"></path>
      <path class="concept-link emphasis" d="M 380 165 C 350 210 350 245 380 280" marker-end="url(#concept-arrow)"></path>
      ${conceptNode(100, 140, "SNA", "Follower ties", "hub exposure")}
      ${conceptNode(380, 140, "ABM", "Agents go online", "view and react")}
      ${conceptNode(660, 140, "Curation", "Chronological", "belief, popularity")}
      ${conceptNode(470, 300, "Diffusion", "Story activity", "Phi curves")}
      ${conceptNode(190, 300, "Validation", "Observed traces", "RMSE, NRMSE")}
      <g class="concept-center">
        <circle cx="380" cy="222" r="44"></circle>
        <text x="380" y="215">
          <tspan x="380">Research</tspan>
          <tspan x="380" dy="17">questions</tspan>
        </text>
      </g>
    </svg>`;
}

function conceptNode(x, y, title, lineOne, lineTwo) {
  return `
    <g class="concept-node" transform="translate(${x - 74} ${y - 48})">
      <rect width="148" height="96" rx="8"></rect>
      <text x="74" y="30">
        <tspan class="node-title" x="74">${title}</tspan>
        <tspan x="74" dy="22">${lineOne}</tspan>
        <tspan x="74" dy="18">${lineTwo}</tspan>
      </text>
    </g>`;
}

function abmLoopSvg() {
  const steps = [
    [112, 76, "1", "Agents", "states and beliefs"],
    [336, 76, "2", "Network", "followee posts"],
    [336, 220, "3", "Feed", "ranked candidates"],
    [112, 220, "4", "React", "reshare, deny, update"]
  ];
  return `
    <svg class="loop-svg" viewBox="0 0 448 300" role="img" aria-label="Agent-based simulation tick loop">
      <defs>
        <marker id="loop-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z"></path>
        </marker>
      </defs>
      <path class="loop-link" d="M 180 76 H 268" marker-end="url(#loop-arrow)"></path>
      <path class="loop-link" d="M 336 112 V 184" marker-end="url(#loop-arrow)"></path>
      <path class="loop-link" d="M 268 220 H 180" marker-end="url(#loop-arrow)"></path>
      <path class="loop-link" d="M 112 184 V 112" marker-end="url(#loop-arrow)"></path>
      ${steps.map(([x, y, number, title, note]) => loopNode(x, y, number, title, note)).join("")}
      <g class="loop-metric">
        <rect x="156" y="126" width="136" height="48" rx="8"></rect>
        <text x="224" y="146">
          <tspan x="224">Record Phi,</tspan>
          <tspan x="224" dy="16">purity, states</tspan>
        </text>
      </g>
    </svg>`;
}

function loopNode(x, y, number, title, note) {
  return `
    <g class="loop-node" transform="translate(${x - 68} ${y - 36})">
      <rect width="136" height="72" rx="8"></rect>
      <circle cx="24" cy="24" r="13"></circle>
      <text class="loop-number" x="24" y="29">${number}</text>
      <text x="78" y="27">
        <tspan class="node-title" x="78">${title}</tspan>
        <tspan x="78" dy="19">${note}</tspan>
      </text>
    </g>`;
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

function renderCurationInterventions(data, cases) {
  const container = document.getElementById("curation-intervention-grid");
  const verdicts = data.phase6?.verdict_rows ?? [];
  const targetRows = verdicts.filter((row) =>
    row.metric?.startsWith("change_") && row.feed_algorithm !== "chronological"
  );
  if (!targetRows.length) {
    container.innerHTML = `<article class="chart-card"><p class="case-meta">Run Phase 6 with paper targets to compare curation interventions.</p></article>`;
    return;
  }
  const targetIndex = new Map(
    targetRows.map((row) => [
      `${row.case_name}:${row.feed_algorithm}:${row.metric}`,
      row
    ])
  );
  const maxAbs = Math.max(
    0.1,
    ...targetRows.flatMap((row) => [
      Math.abs(Number(row.target_value ?? 0)),
      Math.abs(Number(row.actual_value ?? 0))
    ])
  );
  const metrics = [
    ["change_phi_avg", "Phi avg"],
    ["change_phi_max", "Phi max"],
    ["change_belief_purity", "Purity"]
  ];
  container.innerHTML = cases
    .map((item) => {
      const rows = (item.feed_relative_changes ?? [])
        .filter((row) => row.feed_algorithm !== "chronological");
      return `
        <article class="intervention-card">
          <div class="chart-card-head">
            <div>
              <span class="tag ${item.label === "false" ? "next" : "complete"}">${item.label}</span>
              <h3>${titleize(item.case_name)}</h3>
            </div>
            <p class="chart-stat">${rows.length} interventions</p>
          </div>
          <div class="intervention-list">
            ${rows.map((row) => interventionRow(item.case_name, row, metrics, targetIndex, maxAbs)).join("")}
          </div>
        </article>`;
    })
    .join("");
}

function interventionRow(caseName, row, metrics, targetIndex, maxAbs) {
  return `
    <div class="intervention-row">
      <div class="intervention-feed">${titleize(row.feed_algorithm)}</div>
      <div class="intervention-metrics">
        ${metrics.map(([metric, label]) => {
          const target = targetIndex.get(`${caseName}:${row.feed_algorithm}:${metric}`);
          const actualValue = row[metric] ?? target?.actual_value ?? 0;
          return pairedInterventionBar(label, Number(actualValue), Number(target?.target_value ?? 0), maxAbs, target?.verdict ?? "blocked");
        }).join("")}
      </div>
    </div>`;
}

function pairedInterventionBar(label, actual, target, maxAbs, verdict) {
  const targetWidth = Math.min(50, Math.abs(target / maxAbs) * 50);
  const actualWidth = Math.min(50, Math.abs(actual / maxAbs) * 50);
  const targetStyle = target >= 0
    ? `left:50%;width:${targetWidth}%`
    : `left:${50 - targetWidth}%;width:${targetWidth}%`;
  const actualStyle = actual >= 0
    ? `left:50%;width:${actualWidth}%`
    : `left:${50 - actualWidth}%;width:${actualWidth}%`;
  return `
    <div class="intervention-metric">
      <div class="intervention-label">
        <span>${label}</span>
        <strong class="${statusClass(verdict)}">${verdict}</strong>
      </div>
      <div class="paired-track">
        <i class="zero"></i>
        <i class="target-bar" style="${targetStyle}"></i>
        <i class="actual-bar" style="${actualStyle}"></i>
      </div>
      <div class="paired-values">
        <span>actual ${formatNumber(actual, 2)}</span>
        <span>paper ${formatNumber(target, 2)}</span>
      </div>
    </div>`;
}

function renderAgentNetworks(cases) {
  const container = document.getElementById("agent-network-grid");
  const casesWithSnapshots = cases.filter((item) => item.network_snapshot);
  if (!casesWithSnapshots.length) {
    container.innerHTML = `<article class="chart-card"><p class="case-meta">Run Phase 6 to generate synthetic network snapshots.</p></article>`;
    return;
  }
  container.innerHTML = casesWithSnapshots
    .map((item) => {
      const snapshot = item.network_snapshot;
      const summary = snapshot.summary ?? {};
      return `
        <article class="network-card">
          <div class="chart-card-head">
            <div>
              <span class="tag ${item.label === "false" ? "next" : "complete"}">${item.label}</span>
              <h3>${titleize(item.case_name)}</h3>
            </div>
            <p class="chart-stat">Avg degree ${formatNumber(summary.avg_followees ?? 0, 1)}</p>
          </div>
          ${agentNetworkSvg(snapshot)}
          <div class="legend">
            <span><i class="node-key believe"></i>Believe</span>
            <span><i class="node-key susceptible"></i>Susceptible</span>
            <span><i class="node-key verified"></i>Verified ring</span>
          </div>
          ${degreeHistogram(snapshot)}
          <p class="case-meta">
            ${formatNumber(summary.n_agents ?? 0, 0)} agents,
            ${formatNumber(summary.edge_count ?? 0, 0)} directed edges,
            max followers ${formatNumber(summary.max_followers ?? 0, 0)}.
          </p>
        </article>`;
    })
    .join("");
}

function renderCascadeSnapshots(cases) {
  const container = document.getElementById("cascade-grid");
  const casesWithSnapshots = cases.filter((item) => item.cascade_snapshot);
  if (!casesWithSnapshots.length) {
    container.innerHTML = `<article class="chart-card"><p class="case-meta">Run Phase 6 to generate observed cascade snapshots.</p></article>`;
    return;
  }
  container.innerHTML = casesWithSnapshots
    .map((item) => {
      const snapshot = item.cascade_snapshot;
      const summary = snapshot.summary ?? {};
      return `
        <article class="network-card">
          <div class="chart-card-head">
            <div>
              <span class="tag ${item.label === "false" ? "next" : "complete"}">${item.label}</span>
              <h3>${titleize(item.case_name)}</h3>
            </div>
            <p class="chart-stat">Depth ${formatNumber(summary.max_depth ?? 0, 0)}</p>
          </div>
          ${cascadeSvg(snapshot)}
          <div class="legend">
            <span><i class="node-key source"></i>Source</span>
            <span><i class="node-key propagation"></i>Propagation</span>
          </div>
          <p class="case-meta">
            Sampled ${formatNumber(summary.sample_node_count ?? 0, 0)} of
            ${formatNumber(summary.observed_event_count ?? 0, 0)} events;
            max timestep ${formatNumber(summary.max_timestep ?? 0, 0)}.
          </p>
        </article>`;
    })
    .join("");
}

function renderPhase6Verdicts(data) {
  const container = document.getElementById("phase6-verdict-grid");
  const verdicts = data.phase6?.verdict_rows ?? [];
  const fidelity = data.phase6?.model_fidelity ?? {};
  if (!verdicts.length) {
    container.innerHTML = `<article class="chart-card"><p class="case-meta">Run Phase 6 to compute target verdicts.</p></article>`;
    return;
  }
  const statusCounts = verdicts.reduce((acc, row) => {
    acc[row.verdict] = (acc[row.verdict] ?? 0) + 1;
    return acc;
  }, {});
  const cards = [
    ["Network", fidelity.network_model ?? "unknown", "Synthetic social graph"],
    ["Beliefs", fidelity.belief_update_mode ?? "unknown", "Belief update mode"],
    ["Nposts", "sampled", `Mean 40, std 20 in Phase 6`],
    ["Verdicts", `${statusCounts.matched ?? 0}/${verdicts.length}`, "Exact target matches"]
  ];
  container.innerHTML = `
    ${cards.map(([label, value, note]) => `
      <article class="metric-card">
        <p class="metric-label">${label}</p>
        <div class="metric-value small">${value}</div>
        <p class="metric-note">${note}</p>
      </article>`).join("")}
    <article class="verdict-table-card">
      <table class="case-table">
        <thead>
          <tr><th>Case</th><th>Feed</th><th>Metric</th><th>Target</th><th>Actual</th><th>Verdict</th></tr>
        </thead>
        <tbody>
          ${verdicts.slice(0, 18).map((row) => `
            <tr>
              <td>${titleize(row.case_name ?? "unknown")}</td>
              <td>${titleize(row.feed_algorithm ?? "unknown")}</td>
              <td>${row.metric}</td>
              <td>${row.target_value === null ? "blocked" : formatNumber(row.target_value, 5)}</td>
              <td>${row.actual_value === null ? "n/a" : formatNumber(row.actual_value, 5)}</td>
              <td><span class="tag ${statusClass(row.verdict)}">${row.verdict}</span></td>
            </tr>`).join("")}
        </tbody>
      </table>
    </article>`;
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

function agentNetworkSvg(snapshot) {
  const width = 520;
  const height = 320;
  const nodes = (snapshot.nodes ?? []).slice(0, 120);
  const nodeIds = new Set(nodes.map((node) => node.id));
  if (!nodes.length) return `<div class="empty-chart">No network sample</div>`;
  const maxFollowers = Math.max(...nodes.map((node) => node.followers), 1);
  const hubs = [...nodes]
    .sort((left, right) => right.followers - left.followers)
    .slice(0, 10);
  const hubIds = new Set(hubs.map((node) => node.id));
  const edges = (snapshot.edges ?? [])
    .filter((edge) =>
      nodeIds.has(edge.source) &&
      nodeIds.has(edge.target) &&
      (hubIds.has(edge.source) || hubIds.has(edge.target))
    )
    .slice(0, 220);
  const positions = new Map();
  hubs.forEach((node, index) => {
    const angle = (index / hubs.length) * Math.PI * 2;
    const radius = 62;
    positions.set(node.id, {
      x: width / 2 + Math.cos(angle) * radius,
      y: height / 2 + Math.sin(angle) * radius
    });
  });
  const remaining = nodes.filter((node) => !hubIds.has(node.id));
  const stateOrder = ["believe", "susceptible", "deny", "cured"];
  stateOrder.forEach((state, stateIndex) => {
    const stateNodes = remaining.filter((node) => node.state === state);
    const ringRadius = 118 + stateIndex * 18;
    const startAngle = -Math.PI / 2 + stateIndex * 0.35;
    stateNodes.forEach((node, index) => {
      const angle = startAngle + (index / Math.max(1, stateNodes.length)) * Math.PI * 2;
      positions.set(node.id, {
        x: width / 2 + Math.cos(angle) * ringRadius,
        y: height / 2 + Math.sin(angle) * ringRadius * 0.72
      });
    });
  });
  const edgeLines = edges.map((edge) => {
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    if (!source || !target) return "";
    const hubEdge = hubIds.has(edge.source) || hubIds.has(edge.target);
    return `<line class="network-edge ${hubEdge ? "hub-edge" : ""}" x1="${source.x.toFixed(1)}" y1="${source.y.toFixed(1)}" x2="${target.x.toFixed(1)}" y2="${target.y.toFixed(1)}"></line>`;
  }).join("");
  const nodeCircles = nodes.map((node) => {
    const point = positions.get(node.id);
    const radius = hubIds.has(node.id)
      ? 6 + Math.min(8, (node.followers / maxFollowers) * 8)
      : 2.6 + Math.min(5, (node.followers / maxFollowers) * 5);
    if (!point) return "";
    return `
      <circle class="network-node ${node.state} ${hubIds.has(node.id) ? "hub" : ""} ${node.verified ? "verified" : ""}"
        cx="${point.x.toFixed(1)}" cy="${point.y.toFixed(1)}" r="${radius.toFixed(1)}">
        <title>${node.id}: ${node.state}, followers ${node.followers}</title>
      </circle>`;
  }).join("");
  const labels = hubs.slice(0, 4).map((node) => {
    const point = positions.get(node.id);
    if (!point) return "";
    return `<text class="hub-label" x="${point.x.toFixed(1)}" y="${(point.y - 12).toFixed(1)}">${node.followers}</text>`;
  }).join("");
  return `
    <svg class="network-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Synthetic agent network sample">
      <circle class="network-ring inner" cx="${width / 2}" cy="${height / 2}" r="72"></circle>
      <ellipse class="network-ring outer" cx="${width / 2}" cy="${height / 2}" rx="190" ry="122"></ellipse>
      <g>${edgeLines}</g>
      <g>${nodeCircles}</g>
      <g>${labels}</g>
    </svg>`;
}

function degreeHistogram(snapshot) {
  const nodes = snapshot.nodes ?? [];
  if (!nodes.length) return "";
  const buckets = [0, 0, 0, 0, 0];
  const maxFollowers = Math.max(...nodes.map((node) => node.followers), 1);
  nodes.forEach((node) => {
    const index = Math.min(4, Math.floor((node.followers / maxFollowers) * 5));
    buckets[index] += 1;
  });
  const maxBucket = Math.max(...buckets, 1);
  return `
    <div class="degree-strip" aria-label="Sample degree distribution">
      ${buckets.map((count, index) => `
        <span>
          <i style="height:${Math.max(8, (count / maxBucket) * 42)}px"></i>
          <b>${index + 1}</b>
        </span>`).join("")}
    </div>`;
}

function cascadeSvg(snapshot) {
  const width = 520;
  const height = 320;
  const nodes = snapshot.nodes ?? [];
  const edges = snapshot.edges ?? [];
  if (!nodes.length) return `<div class="empty-chart">No cascade sample</div>`;
  const byDepth = nodes.reduce((acc, node) => {
    acc[node.depth] = acc[node.depth] ?? [];
    acc[node.depth].push(node);
    return acc;
  }, {});
  const maxDepth = Math.max(...nodes.map((node) => node.depth), 1);
  const positions = new Map();
  Object.entries(byDepth).forEach(([depthKey, depthNodes]) => {
    const depth = Number(depthKey);
    depthNodes.forEach((node, index) => {
      const gap = height / (depthNodes.length + 1);
      positions.set(node.id, {
        x: 28 + (depth / maxDepth) * (width - 56),
        y: gap * (index + 1)
      });
    });
  });
  const edgeLines = edges.map((edge) => {
    const source = positions.get(edge.source);
    const target = positions.get(edge.target);
    if (!source || !target) return "";
    return `<line class="cascade-edge" x1="${source.x.toFixed(1)}" y1="${source.y.toFixed(1)}" x2="${target.x.toFixed(1)}" y2="${target.y.toFixed(1)}"></line>`;
  }).join("");
  const nodeCircles = nodes.map((node) => {
    const point = positions.get(node.id);
    const radius = node.event_type === "source" ? 7 : 3 + Math.min(6, node.child_count);
    return `
      <circle class="cascade-node ${node.event_type}"
        cx="${point.x.toFixed(1)}" cy="${point.y.toFixed(1)}" r="${radius}">
        <title>${node.id}: ${node.event_type}, t=${node.timestep}, children ${node.child_count}</title>
      </circle>`;
  }).join("");
  return `
    <svg class="network-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Observed cascade sample">
      <g>${edgeLines}</g>
      <g>${nodeCircles}</g>
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

function mergePhase6Cases(cases) {
  return cases.map((item) => ({
    ...item,
    simulated_feeds: item.phase6_simulated_feeds ?? item.simulated_feeds,
    feed_relative_changes: item.phase6_feed_relative_changes ?? item.feed_relative_changes
  }));
}

setupTabs();
renderConcepts();
renderProposal();

loadData()
  .then((data) => {
    const displayCases = mergePhase6Cases(data.cases);
    renderSummary(data);
    renderPhases(data.phases);
    renderFaithfulness(data.faithfulness);
    renderProvenance(data.provenance);
    renderCases(displayCases);
    renderPhiCharts(displayCases);
    renderCurationInterventions(data, displayCases);
    renderAgentNetworks(data.cases);
    renderCascadeSnapshots(data.cases);
    renderPhase6Verdicts(data);
    renderRelativeChanges(displayCases);
    renderFakeNewsNetAudit(data.fakenewsnet_audit ?? []);
  })
  .catch((error) => {
    document.body.innerHTML = `<main><h1>Dashboard data error</h1><p>${error.message}</p></main>`;
  });
