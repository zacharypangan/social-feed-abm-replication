"""Social-feed ABM scaffold.

Phase 1 kept this intentionally lightweight. Phase 3 adds traceable state,
event, belief-update, and popularity-feedback mechanics while preserving the
same dependency-light public API.
"""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass, field
from statistics import mean

from social_feed_abm.feed_algorithms import FeedPost, rank_feed
from social_feed_abm.metrics import belief_purity, phi


@dataclass
class Agent:
    """One synthetic social-media agent."""

    agent_id: int
    belief: float
    state: str = "susceptible"
    followees: set[int] = field(default_factory=set)
    followers: set[int] = field(default_factory=set)
    posts: list[FeedPost] = field(default_factory=list)
    story_tweet_count: int = 0
    verified: bool = False


@dataclass(frozen=True)
class SimulationParams:
    """Parameters needed for one simulation run."""

    n_agents: int
    avg_followees: int
    avg_viewed_posts: int
    timesteps: int
    initial_infected: float
    p_online: float
    p_reshare: float
    p_reject: float
    seed: int
    belief_acceptance_distance: float = 0.35
    belief_update_rate: float = 0.15
    belief_update_mode: str = "linear"
    recent_posts_per_followee: int = 3
    verified_probability: float = 0.0
    verified_influence_multiplier: float = 1.0
    popularity_feedback: bool = True
    network_model: str = "barabasi_albert"
    avg_viewed_posts_std: float = 0.0
    probability_sampling: bool = False
    probability_std_fraction: float = 0.0
    background_posts_per_agent: int = 0
    background_post_probability: float = 0.0
    include_network_snapshot: bool = False
    network_snapshot_max_nodes: int = 150
    network_snapshot_max_edges: int = 350


def run_simulation(params: SimulationParams, feed_algorithm: str) -> dict[str, object]:
    """Run one deterministic-seed simulation for one feed algorithm."""

    rng = random.Random(params.seed)
    agents = _make_agents(params, rng)
    _seed_background_posts(agents, params.background_posts_per_agent, rng)
    _seed_initial_believers(agents, params.initial_infected, rng)

    phi_by_timestep: list[float] = []
    purity_by_timestep: list[float] = []
    event_counts_by_timestep: list[dict[str, int]] = []
    state_counts_by_timestep: list[dict[str, int]] = []
    total_story_tweets = 0

    for timestep in range(params.timesteps):
        timestep_story_tweets = 0
        timestep_purities: list[float] = []
        event_counts = {
            "online": 0,
            "feed_view": 0,
            "belief_update": 0,
            "reshare": 0,
            "reject": 0,
            "believe": 0,
            "deny": 0,
        }

        for agent in agents:
            p_online = _sample_probability(params.p_online, params, rng)
            if rng.random() >= p_online:
                continue

            event_counts["online"] += 1
            feed = _candidate_feed(agent, agents, params.recent_posts_per_followee)
            ranked = rank_feed(feed_algorithm, feed, agent.belief, rng)
            viewed_count = _sample_viewed_post_count(params, rng)
            viewed = ranked[:viewed_count]
            if viewed:
                event_counts["feed_view"] += 1
                timestep_purities.append(
                    belief_purity(agent.belief, [post.belief_value for post in viewed])
                )
                if _update_belief(
                    agent,
                    viewed,
                    params.belief_update_rate,
                    params.belief_update_mode,
                ):
                    event_counts["belief_update"] += 1

            p_reject = _sample_probability(params.p_reject, params, rng)
            p_reshare = _sample_probability(params.p_reshare, params, rng)
            p_reshare *= _verified_multiplier(viewed, params.verified_influence_multiplier)
            p_reshare = _clip_probability(p_reshare)

            if agent.state == "believe" and rng.random() < p_reject:
                agent.state = "cured"
                event_counts["reject"] += 1
                _maybe_add_background_post(agent, timestep, params, rng)
                continue

            if agent.state == "believe" and rng.random() < p_reshare:
                _add_story_post(agent, timestep, viewed, rng, params.popularity_feedback)
                timestep_story_tweets += 1
                event_counts["reshare"] += 1
                _maybe_add_background_post(agent, timestep, params, rng)
                continue

            if agent.state == "susceptible" and viewed:
                accepted = _accepts_story(agent, viewed, params.belief_acceptance_distance)
                if accepted and rng.random() < p_reshare:
                    agent.state = "believe"
                    _add_story_post(agent, timestep, viewed, rng, params.popularity_feedback)
                    event_counts["believe"] += 1
                    event_counts["reshare"] += 1
                    timestep_story_tweets += 1
                elif not accepted:
                    agent.state = "deny"
                    event_counts["deny"] += 1

            if agent.state == "deny" and viewed and rng.random() < p_reject:
                agent.state = "cured"
                event_counts["reject"] += 1
            _maybe_add_background_post(agent, timestep, params, rng)

        total_story_tweets += timestep_story_tweets
        phi_by_timestep.append(phi(timestep_story_tweets, params.n_agents))
        purity_by_timestep.append(mean(timestep_purities) if timestep_purities else 0.0)
        event_counts_by_timestep.append(event_counts)
        state_counts_by_timestep.append(_state_counts(agents))

    result = {
        "feed_algorithm": feed_algorithm,
        "timesteps": params.timesteps,
        "phi_by_timestep": phi_by_timestep,
        "belief_purity_by_timestep": purity_by_timestep,
        "event_counts_by_timestep": event_counts_by_timestep,
        "state_counts_by_timestep": state_counts_by_timestep,
        "network_summary": _network_summary(agents),
        "phi_avg": mean(phi_by_timestep) if phi_by_timestep else 0.0,
        "phi_max": max(phi_by_timestep) if phi_by_timestep else 0.0,
        "belief_purity_avg": mean(purity_by_timestep) if purity_by_timestep else 0.0,
        "total_story_tweets": total_story_tweets,
    }
    if params.include_network_snapshot:
        result["network_snapshot"] = network_snapshot(
            agents,
            params.network_snapshot_max_nodes,
            params.network_snapshot_max_edges,
        )
    return result


def summarize_runs(runs: Iterable[dict[str, object]]) -> dict[str, float]:
    """Aggregate repeated run summaries for one case/feed condition."""

    run_list = list(runs)
    if not run_list:
        return {
            "phi_avg_mean": 0.0,
            "phi_max_mean": 0.0,
            "belief_purity_avg_mean": 0.0,
            "total_story_tweets_mean": 0.0,
            "online_events_mean": 0.0,
            "reshare_events_mean": 0.0,
            "believe_events_mean": 0.0,
            "deny_events_mean": 0.0,
        }
    return {
        "phi_avg_mean": mean(float(run["phi_avg"]) for run in run_list),
        "phi_max_mean": mean(float(run["phi_max"]) for run in run_list),
        "belief_purity_avg_mean": mean(
            float(run["belief_purity_avg"]) for run in run_list
        ),
        "total_story_tweets_mean": mean(
            float(run["total_story_tweets"]) for run in run_list
        ),
        "online_events_mean": _mean_event_total(run_list, "online"),
        "reshare_events_mean": _mean_event_total(run_list, "reshare"),
        "believe_events_mean": _mean_event_total(run_list, "believe"),
        "deny_events_mean": _mean_event_total(run_list, "deny"),
    }


def _make_agents(params: SimulationParams, rng: random.Random) -> list[Agent]:
    agents = [Agent(agent_id=i, belief=rng.random()) for i in range(params.n_agents)]
    for agent in agents:
        agent.verified = rng.random() < params.verified_probability

    if params.network_model != "barabasi_albert":
        raise ValueError(f"Unknown network model: {params.network_model}")
    _wire_barabasi_albert(agents, params.avg_followees, rng)

    return agents


def _wire_barabasi_albert(
    agents: list[Agent],
    target_avg_followees: int,
    rng: random.Random,
) -> None:
    """Create a directed follower/followee projection from a BA graph.

    The original paper describes a Barabasi-Albert social network. This
    implementation builds an undirected preferential-attachment backbone and
    projects each edge in both directions so feed visibility remains explicit.
    """

    n_agents = len(agents)
    if n_agents <= 1:
        return
    m = max(1, min(n_agents - 1, round(target_avg_followees / 2)))
    initial_size = min(n_agents, max(2, m + 1))

    repeated: list[int] = []
    for source_id in range(initial_size):
        for target_id in range(source_id + 1, initial_size):
            _add_mutual_connection(agents, source_id, target_id)

    for agent in agents[:initial_size]:
        repeated.extend([agent.agent_id] * len(agent.followees))
    if not repeated:
        repeated = list(range(initial_size))

    for agent_id in range(initial_size, n_agents):
        targets: set[int] = set()
        target_count = min(m, agent_id)
        while len(targets) < target_count:
            targets.add(rng.choice(repeated))
        for target_id in targets:
            _add_mutual_connection(agents, agent_id, target_id)
        repeated.extend(targets)
        repeated.extend([agent_id] * len(targets))


def _add_mutual_connection(
    agents: list[Agent],
    source_id: int,
    target_id: int,
) -> None:
    if source_id == target_id:
        return
    agents[source_id].followees.add(target_id)
    agents[source_id].followers.add(target_id)
    agents[target_id].followees.add(source_id)
    agents[target_id].followers.add(source_id)


def _seed_initial_believers(
    agents: list[Agent],
    initial_infected: float,
    rng: random.Random,
) -> None:
    infected_count = max(1, round(len(agents) * initial_infected))
    for agent in rng.sample(agents, infected_count):
        agent.state = "believe"
        _add_story_post(agent, timestamp=0)


def _seed_background_posts(
    agents: list[Agent],
    posts_per_agent: int,
    rng: random.Random,
) -> None:
    if posts_per_agent <= 0:
        return
    for agent in agents:
        for _ in range(posts_per_agent):
            _add_background_post(agent, -rng.randrange(1, 20), rng)


def _candidate_feed(
    agent: Agent,
    agents: list[Agent],
    recent_posts_per_followee: int,
) -> list[FeedPost]:
    posts: list[FeedPost] = []
    for followee_id in agent.followees:
        posts.extend(agents[followee_id].posts[-recent_posts_per_followee:])
    return posts


def _add_story_post(
    agent: Agent,
    timestamp: int,
    viewed_posts: list[FeedPost] | None = None,
    rng: random.Random | None = None,
    popularity_feedback: bool = True,
) -> None:
    agent.story_tweet_count += 1
    source_post = _choose_source_post(viewed_posts, rng) if viewed_posts else None
    if source_post and popularity_feedback:
        source_post.retweet_count += 1

    post = FeedPost(
        author_id=agent.agent_id,
        timestamp=timestamp,
        belief_value=agent.belief,
        retweet_count=agent.story_tweet_count,
        follower_count=len(agent.followers),
        story_id=source_post.story_id if source_post else "story",
        source_author_id=source_post.author_id if source_post else agent.agent_id,
        is_story=True,
        verified_author=agent.verified,
    )
    agent.posts.append(post)


def _add_background_post(
    agent: Agent,
    timestamp: int,
    rng: random.Random,
) -> None:
    post = FeedPost(
        author_id=agent.agent_id,
        timestamp=timestamp,
        belief_value=min(1.0, max(0.0, rng.gauss(agent.belief, 0.12))),
        retweet_count=rng.randrange(0, 4),
        follower_count=len(agent.followers),
        story_id="background",
        source_author_id=agent.agent_id,
        is_story=False,
        verified_author=agent.verified,
    )
    agent.posts.append(post)


def _maybe_add_background_post(
    agent: Agent,
    timestep: int,
    params: SimulationParams,
    rng: random.Random,
) -> None:
    if params.background_post_probability <= 0:
        return
    if rng.random() < params.background_post_probability:
        _add_background_post(agent, timestep, rng)


def _choose_source_post(
    viewed_posts: list[FeedPost] | None,
    rng: random.Random | None,
) -> FeedPost | None:
    if not viewed_posts:
        return None
    if rng is None:
        return viewed_posts[0]
    story_posts = [post for post in viewed_posts if post.is_story]
    candidates = story_posts if story_posts else viewed_posts
    return rng.choice(candidates)


def _update_belief(
    agent: Agent,
    viewed_posts: list[FeedPost],
    belief_update_rate: float,
    belief_update_mode: str = "linear",
) -> bool:
    if belief_update_rate <= 0:
        return False
    viewed_mean = mean(post.belief_value for post in viewed_posts)
    previous = agent.belief
    if belief_update_mode == "linear":
        target = viewed_mean
    elif belief_update_mode == "bayesian":
        target = _bayesian_posterior(agent.belief, viewed_mean)
    else:
        raise ValueError(f"Unknown belief update mode: {belief_update_mode}")
    agent.belief += belief_update_rate * (target - agent.belief)
    agent.belief = min(1.0, max(0.0, agent.belief))
    return abs(agent.belief - previous) > 1e-12


def _bayesian_posterior(prior: float, evidence: float) -> float:
    prior = min(0.999, max(0.001, prior))
    evidence = min(0.999, max(0.001, evidence))
    likelihood_true = 0.05 + (0.95 * evidence)
    likelihood_false = 0.05 + (0.95 * (1.0 - evidence))
    numerator = prior * likelihood_true
    denominator = numerator + ((1.0 - prior) * likelihood_false)
    if denominator == 0:
        return prior
    return numerator / denominator


def _accepts_story(
    agent: Agent,
    viewed_posts: list[FeedPost],
    belief_acceptance_distance: float,
) -> bool:
    story_posts = [post for post in viewed_posts if post.is_story]
    if not story_posts:
        return False
    viewed_mean = mean(post.belief_value for post in story_posts)
    return abs(agent.belief - viewed_mean) <= belief_acceptance_distance


def _state_counts(agents: list[Agent]) -> dict[str, int]:
    counts = {"susceptible": 0, "believe": 0, "deny": 0, "cured": 0}
    for agent in agents:
        counts[agent.state] = counts.get(agent.state, 0) + 1
    return counts


def _network_summary(agents: list[Agent]) -> dict[str, float]:
    if not agents:
        return {
            "n_agents": 0,
            "avg_followees": 0.0,
            "avg_followers": 0.0,
            "max_followers": 0.0,
            "verified_count": 0.0,
        }
    followee_counts = [len(agent.followees) for agent in agents]
    follower_counts = [len(agent.followers) for agent in agents]
    return {
        "n_agents": float(len(agents)),
        "edge_count": float(sum(followee_counts)),
        "avg_followees": mean(followee_counts),
        "avg_followers": mean(follower_counts),
        "max_followers": float(max(follower_counts)),
        "min_followers": float(min(follower_counts)),
        "verified_count": float(sum(1 for agent in agents if agent.verified)),
    }


def network_snapshot(
    agents: list[Agent],
    max_nodes: int = 150,
    max_edges: int = 350,
) -> dict[str, object]:
    """Build a public-safe diagnostic snapshot of the synthetic agent network."""

    if max_nodes <= 0:
        raise ValueError("max_nodes must be positive")
    if max_edges <= 0:
        raise ValueError("max_edges must be positive")
    ranked = sorted(
        agents,
        key=lambda agent: (
            len(agent.followers),
            agent.story_tweet_count,
            agent.verified,
            -agent.agent_id,
        ),
        reverse=True,
    )
    selected = sorted(agent.agent_id for agent in ranked[:max_nodes])
    selected_set = set(selected)
    nodes = [
        {
            "id": _agent_public_id(agent_id),
            "agent_id": _agent_public_id(agent_id),
            "state": agents[agent_id].state,
            "belief_bucket": _belief_bucket(agents[agent_id].belief),
            "verified": agents[agent_id].verified,
            "followers": len(agents[agent_id].followers),
            "followees": len(agents[agent_id].followees),
            "story_tweet_count": agents[agent_id].story_tweet_count,
        }
        for agent_id in selected
    ]
    edges: list[dict[str, object]] = []
    seen: set[tuple[int, int]] = set()
    for source_id in selected:
        for target_id in sorted(agents[source_id].followees):
            if target_id not in selected_set:
                continue
            signature = (source_id, target_id)
            if signature in seen:
                continue
            seen.add(signature)
            edges.append(
                {
                    "source": _agent_public_id(source_id),
                    "target": _agent_public_id(target_id),
                }
            )
            if len(edges) >= max_edges:
                break
        if len(edges) >= max_edges:
            break
    return {
        "type": "synthetic_agent_network",
        "model": "barabasi_albert_directed_projection",
        "summary": _network_summary(agents),
        "sample": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "max_nodes": max_nodes,
            "max_edges": max_edges,
        },
        "nodes": nodes,
        "edges": edges,
    }


def _sample_viewed_post_count(params: SimulationParams, rng: random.Random) -> int:
    if params.avg_viewed_posts_std <= 0:
        return max(0, params.avg_viewed_posts)
    sampled = round(rng.gauss(params.avg_viewed_posts, params.avg_viewed_posts_std))
    return max(1, min(max(1, params.avg_viewed_posts * 3), sampled))


def _sample_probability(
    probability: float,
    params: SimulationParams,
    rng: random.Random,
) -> float:
    if not params.probability_sampling or params.probability_std_fraction <= 0:
        return _clip_probability(probability)
    std = max(0.0, probability * params.probability_std_fraction)
    return _clip_probability(rng.gauss(probability, std))


def _verified_multiplier(
    viewed_posts: list[FeedPost],
    multiplier: float,
) -> float:
    if multiplier <= 1.0:
        return 1.0
    if any(post.is_story and post.verified_author for post in viewed_posts):
        return multiplier
    return 1.0


def _clip_probability(value: float) -> float:
    return min(1.0, max(0.0, value))


def _agent_public_id(agent_id: int) -> str:
    return f"agent_{agent_id:04d}"


def _belief_bucket(value: float) -> str:
    if value < 0.33:
        return "low"
    if value < 0.67:
        return "medium"
    return "high"


def _mean_event_total(
    runs: list[dict[str, object]],
    event_name: str,
) -> float:
    totals: list[int] = []
    for run in runs:
        event_counts = run.get("event_counts_by_timestep", [])
        if not isinstance(event_counts, list):
            continue
        total = 0
        for row in event_counts:
            if isinstance(row, dict):
                total += int(row.get(event_name, 0))
        totals.append(total)
    return mean(totals) if totals else 0.0
