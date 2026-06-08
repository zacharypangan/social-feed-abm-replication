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
    recent_posts_per_followee: int = 3
    verified_probability: float = 0.0
    popularity_feedback: bool = True


def run_simulation(params: SimulationParams, feed_algorithm: str) -> dict[str, object]:
    """Run one deterministic-seed simulation for one feed algorithm."""

    rng = random.Random(params.seed)
    agents = _make_agents(params, rng)
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
            if rng.random() >= params.p_online:
                continue

            event_counts["online"] += 1
            feed = _candidate_feed(agent, agents, params.recent_posts_per_followee)
            ranked = rank_feed(feed_algorithm, feed, agent.belief, rng)
            viewed = ranked[: params.avg_viewed_posts]
            if viewed:
                event_counts["feed_view"] += 1
                timestep_purities.append(
                    belief_purity(agent.belief, [post.belief_value for post in viewed])
                )
                if _update_belief(agent, viewed, params.belief_update_rate):
                    event_counts["belief_update"] += 1

            if agent.state == "believe" and rng.random() < params.p_reject:
                agent.state = "cured"
                event_counts["reject"] += 1
                continue

            if agent.state == "believe" and rng.random() < params.p_reshare:
                _add_story_post(agent, timestep, viewed, rng, params.popularity_feedback)
                timestep_story_tweets += 1
                event_counts["reshare"] += 1
                continue

            if agent.state == "susceptible" and viewed:
                accepted = _accepts_story(agent, viewed, params.belief_acceptance_distance)
                if accepted and rng.random() < params.p_reshare:
                    agent.state = "believe"
                    _add_story_post(agent, timestep, viewed, rng, params.popularity_feedback)
                    event_counts["believe"] += 1
                    event_counts["reshare"] += 1
                    timestep_story_tweets += 1
                elif not accepted:
                    agent.state = "deny"
                    event_counts["deny"] += 1

            if agent.state == "deny" and viewed and rng.random() < params.p_reject:
                agent.state = "cured"
                event_counts["reject"] += 1

        total_story_tweets += timestep_story_tweets
        phi_by_timestep.append(phi(timestep_story_tweets, params.n_agents))
        purity_by_timestep.append(mean(timestep_purities) if timestep_purities else 0.0)
        event_counts_by_timestep.append(event_counts)
        state_counts_by_timestep.append(_state_counts(agents))

    return {
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

    target_followees = min(params.avg_followees, params.n_agents - 1)
    attachment_repeats = [0]

    for agent_id in range(1, params.n_agents):
        existing = list(range(agent_id))
        selected: set[int] = set()
        while len(selected) < min(target_followees, len(existing)):
            selected.add(rng.choice(attachment_repeats))
        agents[agent_id].followees.update(selected)
        for followee_id in selected:
            agents[followee_id].followers.add(agent_id)
        attachment_repeats.extend([agent_id] + list(selected))

    for agent in agents:
        while len(agent.followees) < target_followees:
            candidate = rng.randrange(params.n_agents)
            if candidate != agent.agent_id:
                agent.followees.add(candidate)
                agents[candidate].followers.add(agent.agent_id)

    return agents


def _seed_initial_believers(
    agents: list[Agent],
    initial_infected: float,
    rng: random.Random,
) -> None:
    infected_count = max(1, round(len(agents) * initial_infected))
    for agent in rng.sample(agents, infected_count):
        agent.state = "believe"
        _add_story_post(agent, timestamp=0)


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
    )
    agent.posts.append(post)


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
) -> bool:
    if belief_update_rate <= 0:
        return False
    viewed_mean = mean(post.belief_value for post in viewed_posts)
    previous = agent.belief
    agent.belief += belief_update_rate * (viewed_mean - agent.belief)
    agent.belief = min(1.0, max(0.0, agent.belief))
    return abs(agent.belief - previous) > 1e-12


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
    return {
        "n_agents": float(len(agents)),
        "avg_followees": mean(len(agent.followees) for agent in agents),
        "avg_followers": mean(len(agent.followers) for agent in agents),
        "max_followers": float(max(len(agent.followers) for agent in agents)),
        "verified_count": float(sum(1 for agent in agents if agent.verified)),
    }


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
