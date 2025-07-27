from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from toad._loop import loop_last

type SettingsType = dict[str, object]


@dataclass
class Setting:
    name: str
    type: str
    help: str
    validate: list[dict] | None = None
    choices: list[str] | None = None
    children: list[Setting] | None = None


SCHEMA = {
    "ui": {
        "Help": "User interface settings",
        "type": "object",
        "contents": {
            "column": {
                "help": "Enable column?",
                "type": "boolean",
                "default": True,
            },
            "column-width": {
                "help": "Width of the column, if `column=true`",
                "type": "integer",
                "default": 100,
                "validate": [{"type": "minimum", "value": 40}],
            },
            "theme": {
                "help": "Default Textual theme",
                "type": "string",
                "default": "dracula",
                "choices": [
                    "textual-dark",
                    "textual-light",
                    "nord",
                    "gruvbox",
                    "catppuccin-mocha",
                    "dracula",
                    "tokyo-night",
                    "monokai",
                    "flexoki",
                    "catppuccin-late",
                    "solarized-light",
                ],
            },
        },
    },
    "user": {
        "help": "User information",
        "type": "object",
        "contents": {
            "name": {
                "help": "Your name",
                "type": "string",
                "default": "",
            },
            "email": {
                "help": "Your email",
                "type": "string",
                "validate": [{"type": "is_email"}],
                "default": "",
            },
        },
    },
    "accounts": {
        "help": "User accounts",
        "type": "group",
        "defaults": ["anthropic", "openai"],
        "contents": {
            "key": {
                "type": "string",
                "name": "key",
                "default": "",
                "help": "API Key",
            }
        },
    },
}

INPUT_TYPES = {"boolean", "integer", "string"}


class InvalidKey(Exception):
    """The key is not in the schema."""


def parse_key(key: str) -> Sequence[str]:
    return key.split(".")


def get_setting(settings: dict[str, object], key: str) -> object:
    for last, key in loop_last(parse_key(key)):
        if last:
            return settings[key]
        else:
            settings = settings[key]
    return None


class Schema:
    def __init__(self, schema: SettingsType) -> None:
        self.schema = schema

    def set_value(self, settings: SettingsType, key: str, value: object) -> None:
        schema = self.schema
        keys = parse_key(key)
        for last, key in loop_last(keys):
            if last:
                settings[key] = value
            if key not in schema:
                raise InvalidKey()
            schema = schema[key]
            assert isinstance(schema, dict)
            if key not in settings:
                settings = settings[key] = {}

    def build_default(self) -> SettingsType:
        settings: SettingsType = {}

        def set_defaults(schema: SettingsType, settings: SettingsType) -> None:
            for key, sub_schema in schema.items():
                assert isinstance(sub_schema, dict)
                type = sub_schema["type"]
                if type in INPUT_TYPES:
                    if (default := sub_schema.get("default")) is not None:
                        settings[key] = default

                elif type == "object":
                    if contents := sub_schema.get("contents"):
                        sub_settings = settings[key] = {}
                        set_defaults(contents, sub_settings)

                elif type == "group":
                    data_settings = settings[key] = {}
                    if defaults := sub_schema.get("defaults"):
                        for default in defaults:
                            sub_settings = data_settings[default] = {}
                            if data_schema := sub_schema.get("contents"):
                                set_defaults(data_schema, sub_settings)

        set_defaults(self.schema, settings)

        return settings

    def get_form_settings(self, settings: dict[str, object]) -> Sequence[Setting]:
        form_settings: list[Setting] = []

        def iter_settings(name: str, schema: SettingsType) -> Iterable[Setting]:
            schema_type = schema["type"]
            if schema_type in INPUT_TYPES:
                yield Setting(
                    name,
                    schema["type"],
                    schema.get("help", ""),
                    choices=schema.get("choices"),
                    validate=schema.get("validate"),
                )

            elif schema_type == "object":
                yield Setting(
                    name,
                    schema["type"],
                    schema.get("help", ""),
                    choices=schema.get("choices"),
                    validate=schema.get("validate"),
                    children=[
                        setting
                        for child_name, schema in schema.get("contents", {}).items()
                        for setting in iter_settings(f"{name}.{child_name}", schema)
                    ],
                )

            elif schema_type == "group":
                yield Setting(
                    name,
                    schema["type"],
                    schema.get(help, ""),
                    children=[
                        Setting(
                            f"{name}.{sub_name}",
                            schema["type"],
                            schema.get("help", ""),
                            choices=schema.get("choices"),
                            validate=schema.get("validate"),
                            children=[
                                setting
                                for child_name, schema in schema.get(
                                    "contents", {}
                                ).items()
                                for setting in iter_settings(
                                    f"{name}.{sub_name}.{child_name}", schema
                                )
                            ],
                        )
                        for sub_name in get_setting(settings, name)
                    ],
                )

        for name, schema in self.schema.items():
            form_settings.extend(iter_settings(name, schema))
        return form_settings


if __name__ == "__main__":
    from rich import print
    from rich.traceback import install

    install(show_locals=True, width=None)

    # print(SCHEMA)
    schema = Schema(SCHEMA)
    settings = schema.build_default()
    print(settings)

    print(schema.get_form_settings(settings))
