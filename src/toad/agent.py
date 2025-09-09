from abc import ABC, abstractmethod
from pathlib import Path


class AgentBase(ABC):
    """Base class for an 'agent'."""

    def __init__(self, project_root: Path) -> None:
        self.project_root_path = project_root
        super().__init__()

    @abstractmethod
    async def send_prompt(self, prompt: str) -> None: ...
