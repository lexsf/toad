from importlib.metadata import version
from importlib.resources import files

from textual.screen import Screen
from textual import work
from textual import getters
from textual import on
from textual.app import ComposeResult
from textual.content import Content
from textual import containers
from textual import widgets

from toad.pill import pill
from toad.widgets.mandelbrot import Mandelbrot
from toad.widgets.grid_select import GridSelect
from toad.agent_schema import Agent
from toad.agents import read_agents


QR = """\
█▀▀▀▀▀█ ▄█ ▄▄█▄▄█ █▀▀▀▀▀█
█ ███ █ ▄█▀█▄▄█▄  █ ███ █
█ ▀▀▀ █ ▄ █ ▀▀▄▄▀ █ ▀▀▀ █
▀▀▀▀▀▀▀ ▀ ▀ ▀ █ █ ▀▀▀▀▀▀▀
█▀██▀ ▀█▀█▀▄▄█   ▀ █ ▀ █ 
 █ ▀▄▄▀▄▄█▄▄█▀██▄▄▄▄ ▀ ▀█
▄▀▄▀▀▄▀ █▀▄▄▄▀▄ ▄▀▀█▀▄▀█▀
█ ▄ ▀▀▀█▀ █ ▀ █▀ ▀ ██▀ ▀█
▀  ▀▀ ▀▀▄▀▄▄▀▀▄▀█▀▀▀█▄▀  
█▀▀▀▀▀█ ▀▄█▄▀▀  █ ▀ █▄▀▀█
█ ███ █ ██▄▄▀▀█▀▀██▀█▄██▄
█ ▀▀▀ █ ██▄▄ ▀  ▄▀ ▄▄█▀ █
▀▀▀▀▀▀▀ ▀▀▀  ▀   ▀▀▀▀▀▀▀▀"""


class AgentItem(containers.Vertical):
    """An entry in the Agent grid select."""

    def __init__(self, agent: Agent) -> None:
        self._agent = agent
        super().__init__()

    @property
    def agent(self) -> Agent:
        return self._agent

    def compose(self) -> ComposeResult:
        agent = self._agent
        with containers.Grid():
            yield widgets.Label(agent["name"], id="name")
            yield widgets.Label(
                pill(agent["type"], "$primary-muted", "$text-primary"), id="type"
            )
        yield widgets.Label(agent["author_name"], id="author")
        yield widgets.Static(agent["description"], id="description")


class StoreScreen(Screen):
    CSS_PATH = "store.tcss"

    agents_view = getters.query_one("#agents-view")

    def compose(self) -> ComposeResult:
        with containers.VerticalScroll():
            with containers.VerticalGroup(id="title-container"):
                with containers.Grid(id="title-grid"):
                    yield Mandelbrot()
                    yield widgets.Label(self.get_info(), id="info")
                    # yield widgets.Label(QR, id="qr")
            yield widgets.Static("Agents", classes="heading")
            yield (agents_view := GridSelect(id="agents-view", min_column_width=40))
            agents_view.loading = True
        yield widgets.Footer()

    def get_info(self) -> Content:
        content = Content.assemble(
            Content.from_markup("Toad"),
            pill(f"v{version('toad')}", "$primary-muted", "$text-primary"),
            ("\nThe universal interface for AI in your terminal", "$text-success"),
            (
                "\nSoftware lovingly crafted by hand (with a dash of AI) in Edinburgh, Scotland",
                "dim",
            ),
            "\n",
            (
                Content.from_markup(
                    "\nConsider sponsoring [@click=screen.url('https://github.com/sponsors/willmcgugan')]@willmcgugan[/] to support development of Toad!"
                )
            ),
            "\n\n",
            (
                Content.from_markup(
                    "[dim]Code: [@click=screen.url('https://github.com/Textualize/toad')]Repository[/] "
                    "Bugs: [@click=screen.url('https://github.com/Textualize/toad/discussions')]Discussions[/]"
                )
            ),
        )

        return content

    def action_url(self, url: str) -> None:
        import webbrowser

        webbrowser.open(url)

    async def update_agents_data(self, agents: list[Agent]) -> None:
        """Mount an entry for each Agent.

        Args:
            agents: List of Agent dicts
        """
        agents_view = self.agents_view
        if agents:
            agents = sorted(agents, key=lambda agent: agent["name"].casefold())
            agent_items = [AgentItem(agent) for agent in agents]
            await agents_view.mount_all(agent_items)
            agents_view.highlighted = 0
        agents_view.loading = False

    @on(GridSelect.Selected)
    def on_grid_select_selected(self, event: GridSelect.Selected):
        assert isinstance(event.selected_widget, AgentItem)
        from toad.screens.agent_modal import AgentModal

        self.app.push_screen(AgentModal(event.selected_widget.agent))

    @work
    async def on_mount(self) -> None:
        agents: list[Agent] = []
        try:
            agents = await read_agents()
        except Exception as error:
            self.notify(
                f"Failed to read agents data ({error})",
                title="Agents data",
                severity="error",
            )
        else:
            await self.update_agents_data(agents)


if __name__ == "__main__":
    from textual.app import App

    class StoreApp(App):
        CSS_PATH = "store.tcss"
        DEFAULT_THEME = "dracula"

        def on_ready(self) -> None:
            self.theme = "dracula"

        def get_default_screen(self) -> Screen:
            return StoreScreen()

    StoreApp().run()
