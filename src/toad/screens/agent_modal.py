from typing import cast

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual import containers
from textual import widgets
from textual.reactive import var

import toad
from toad.agent_schema import Agent, OS


class AgentModal(ModalScreen):
    AUTO_FOCUS = "#script-select"

    BINDINGS = [("escape", "dismiss", "Dismiss")]

    action = var("")

    def __init__(self, agent: Agent) -> None:
        self._agent = agent
        super().__init__()

    def compose(self) -> ComposeResult:
        agent = self._agent

        scripts = agent["actions"]

        script_os = cast(OS, toad.os)
        if script_os not in scripts:
            script_os = "*"

        scripts = scripts[cast(OS, script_os)]
        script_choices = [
            (script["description"], name) for name, script in scripts.items()
        ]

        with containers.Vertical(id="container"):
            with containers.VerticalScroll(id="description-container"):
                yield widgets.Markdown(agent["help"], id="description")
            with containers.VerticalGroup():
                with containers.HorizontalGroup():
                    yield widgets.Checkbox("Show in launcher")
                    yield widgets.Select(
                        script_choices,
                        prompt="Actions",
                        allow_blank=True,
                        id="script-select",
                    )
                    yield widgets.Button(
                        "Go", variant="primary", id="run-action", disabled=True
                    )

    @on(widgets.Select.Changed)
    def on_select_changed(self, event: widgets.Select.Changed) -> None:
        self.action = event.value if isinstance(event.value, str) else ""

    def watch_action(self, action: str) -> None:
        go_button = self.query_one("#run-action", widgets.Button)
        go_button.disabled = not action
