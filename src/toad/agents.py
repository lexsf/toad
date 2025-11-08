from importlib.resources import files
import asyncio

from toad.agent_schema import Agent


class AgentReadError(Exception):
    """Problem reading the agents."""


async def read_agents() -> list[Agent]:
    import tomllib

    def read_agents() -> list[Agent]:
        """Read agent information.

        Stored in data/agents

        Returns:
            List of agent dicts.
        """
        agents: list[Agent] = []
        try:
            for file in files("toad.data").joinpath("agents").iterdir():
                agent: Agent = tomllib.load(file.open("rb"))
                agents.append(agent)

        except Exception as error:
            raise AgentReadError(f"Failed to read agents; {error}")

        return agents

    agents = await asyncio.to_thread(read_agents)
    return agents
