from textual import on
from textual.app import ComposeResult
from textual import containers

from textual import getters
from textual.screen import Screen
from textual.reactive import var


from toad.answer import Answer
from toad.widgets.question import Question
from toad.widgets.diff_view import DiffView

from textual.widgets import OptionList, Footer, Static
from textual.widgets.option_list import Option

from toad.app import ToadApp

SOURCE1 = '''\
def loop_first(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first value."""
    iter_values = iter(values)
    try:
        value = next(iter_values)
    except StopIteration:
        return
    yield True, value
    for value in iter_values:
        yield False, value


def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value

'''

SOURCE2 = '''\
def loop_first(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first value.
    
    Args:
        values: iterables of values.

    Returns:
        Iterable of a boolean to indicate first value, and a value from the iterable.
    """
    iter_values = iter(values)
    try:
        value = next(iter_values)
    except StopIteration:
        return
    yield True, value
    for value in iter_values:
        yield False, value


def loop_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value


def loop_first_last(values: Iterable[ValueType]) -> Iterable[tuple[bool, bool, ValueType]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)  # Get previous value
    except StopIteration:
        return
    first = True

'''


class PermissionsScreen(Screen):
    CSS_PATH = "permissions.tcss"

    tool_container = getters.query_one("#tool-container", containers.VerticalScroll)
    navigator = getters.query_one("#navigator", OptionList)
    index: var[int] = var(0)
    app = getters.app(ToadApp)

    def compose(self) -> ComposeResult:
        with containers.Vertical(classes="top"):
            yield Static(
                "[b]Approval request[/b] [dim]The Agent wishes to make the following changes",
                id="instructions",
            )
            with containers.HorizontalGroup(id="changes"):
                yield OptionList(id="navigator")
                yield containers.VerticalScroll(id="tool-container")
            yield Question(
                options=[
                    Answer("Yes, merge this", "merge"),
                    Answer("No, this is rubbish", "no-merge"),
                ]
            )

        yield Footer()

    async def on_mount(self):
        await self.add_diff("foo.py", "foo.py", SOURCE1, SOURCE2)

    async def add_diff(
        self, path1: str, path2: str, before: str | None, after: str
    ) -> None:
        self.index += 1
        option_id = f"item-{self.index}"
        diff_view = DiffView(path1, path2, before or "", after, id=option_id)
        diff_view_setting = self.app.settings.get("diff.view", str)
        diff_view.split = diff_view_setting == "split"
        diff_view.auto_split = diff_view_setting == "auto"
        await self.tool_container.mount(diff_view)
        option_text = f"📄 {path1}"
        self.navigator.add_option(Option(option_text, option_id))

    @on(OptionList.OptionHighlighted)
    def on_option_highlighted(self, event: OptionList.OptionHighlighted):
        self.tool_container.query_one(f"#{event.option_id}").scroll_visible(top=True)


if __name__ == "__main__":
    SOURCE1 = '''\
def loop_first(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first value."""
    iter_values = iter(values)
    try:
        value = next(iter_values)
    except StopIteration:
        return
    yield True, value
    for value in iter_values:
        yield False, value


def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value

'''

    SOURCE2 = '''\
def loop_first(values: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """Iterate and generate a tuple with a flag for first value.
    
    Args:
        values: iterables of values.

    Returns:
        Iterable of a boolean to indicate first value, and a value from the iterable.
    """
    iter_values = iter(values)
    try:
        value = next(iter_values)
    except StopIteration:
        return
    yield True, value
    for value in iter_values:
        yield False, value


def loop_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value


def loop_first_last(values: Iterable[ValueType]) -> Iterable[tuple[bool, bool, ValueType]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)  # Get previous value
    except StopIteration:
        return
    first = True

'''

    from textual.app import App

    class PermissionTestApp(App):
        async def on_mount(self) -> None:
            screen = PermissionsScreen()
            await self.push_screen(screen)
            for repeat in range(5):
                await screen.add_diff("foo.py", "foo.py", SOURCE1, SOURCE2)

    app = PermissionTestApp()
    app.run()
