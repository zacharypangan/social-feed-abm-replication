"""Minimal Phase 1 ABM scaffold.

This is intentionally lightweight. It is a reproducible MVP for exercising the
four feed objectives, not a full calibration-quality reproduction yet.
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


def run_simulation(params: SimulationParams, feed_algorithm: str) -> dict[str, object]:
    """Run one deterministic-seed simulation for one feed algorithm."""

    rng = random.Random(params.seed)
    agents = _make_agents(params, rng)
    _seed_initial_believers(agents, params.initial_infected, rng)

    phi_by_timestep: list[float] = []
    purity_by_timestep: list[float] = []
    total_story_tweets = 0

    for timestep in range(params.timesteps):
        timestep_story_tweets = 0
        timestep_purities: list[float] = []

        for agent in agents:
            if rng.random() >= params.p_online:
                continue

            feed = _candidate_feed(agent, agents)
            ranked = rank_feed(feed_algorithm, feed, agent.belief, rng)
            viewed = ranked[: params.avg_viewed_posts]
            if viewed:
                timestep_purities.append(
                    belief_purity(agent.belief, [post.belief_value for post in viewed])
                )

            if agent.state == "believe" and rng.random() < params.p_reject:
                agent.state = "cured"
                continue

            if agent.state == "believe" and rng.random() < params.p_reshare:
                _add_story_post(agent, timestep)
                timestep_story_tweets += 1
                continue

            if agent.state == "susceptible" and viewed and rng.random() < params.p_reshare:
                agent.state = "believe"
                _add_story_post(agent, timestep)
                timestep_story_tweets += 1

        total_story_tweets += timestep_story_tweets
        phi_by_timestep.append(phi(timestep_story_tweets, params.n_agents))
        purity_by_timestep.append(mean(timestep_purities) if timestep_purities else 0.0)

    return {
        "feed_algorithm": feed_algorithm,
        "timesteps": params.timesteps,
        "phi_by_timestep": phi_by_timestep,
        "belief_purity_by_timestep": purity_by_timestep,
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
        }
    return {
        "phi_avg_mean": mean(float(run["phi_avg"]) for run in run_list),
        "phi_max_mean": mean(float(run["phi_max"]) for run in run_list),
        "belief_purity_avg_mean": mean(
            float(run["belief_purity_avg"]) for run in run_list
        ),
    }


def _make_agents(params: SimulationParams, rng: random.Random) -> list[Agent]:
    agents = [Agent(agent_id=i, belief=rng.random()) for i in range(params.n_agents)]
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


def _candidate_feed(agent: Agent, agents: list[Agent]) -> list[FeedPost]:
    posts: list[FeedPost] = []
    for followee_id in agent.followees:
        posts.extend(agents[followee_id].posts[-3:])
    return posts


def _add_story_post(agent: Agent, timestamp: int) -> None:
    agent.story_tweet_count += 1
    post = FeedPost(
        author_id=agent.agent_id,
        timestamp=timestamp,
        belief_value=agent.belief,
        retweet_count=agent.story_tweet_count,
        follower_count=len(agent.followers),
    )
    agent.posts.append(post)
