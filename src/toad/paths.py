from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home, xdg_state_home


APP_NAME = "toad"


def path_to_name(path: Path) -> str:
    """Converts a path to a name (suitable as a path component).

    Args:
        path: A path.

    Returns:
        A stringified version of the path.
    """
    name = str(path.resolve()).replace("/", "-")
    return name


def get_data() -> Path:
    """Return (possibly creating) the application data directory."""
    path = xdg_data_home() / APP_NAME
    path.mkdir(0o700, exist_ok=True, parents=True)
    return path


def get_config() -> Path:
    """Return (possibly creating) the application config directory."""
    path = xdg_config_home() / APP_NAME
    path.mkdir(0o700, exist_ok=True, parents=True)
    return path


def get_state(self) -> Path:
    """Return (possibly creating) the application state directory."""
    path = xdg_state_home() / APP_NAME
    path.mkdir(0o700, exist_ok=True, parents=True)
    return path
