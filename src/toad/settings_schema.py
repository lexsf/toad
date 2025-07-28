from toad.settings import SchemaDict

SCHEMA: list[SchemaDict] = [
    {
        "key": "ui",
        "title": "User interface settings",
        "type": "object",
        "fields": [
            {
                "key": "column",
                "title": "Enable column?",
                "help": "Enable for a fixed column size. Disable to use the full screen width.",
                "type": "boolean",
                "default": True,
            },
            {
                "key": "column-width",
                "title": "Width of the column",
                "help": "Width of the column if enabled.",
                "type": "integer",
                "default": 100,
                "validate": [{"type": "minimum", "value": 40}],
            },
            {
                "key": "theme",
                "title": "Theme",
                "help": "One of the builtin Textual themes.",
                "type": "choices",
                "default": "dracula",
                "validate": [
                    {
                        "type": "choices",
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
                    }
                ],
            },
        ],
    },
    {
        "key": "user",
        "title": "User information",
        "help": "Your details.",
        "type": "object",
        "fields": [
            {
                "key": "name",
                "title": "Your name",
                "type": "string",
                "default": "$USER",
            },
            {
                "key": "email",
                "title": "Your email",
                "type": "string",
                "validate": [{"type": "is_email"}],
                "default": "",
            },
        ],
    },
    {
        "key": "accounts",
        "title": "User accounts",
        "help": "Account information used by AI services.",
        "type": "list",
        "default": [
            {"key": "anthropic", "apikey": "$ANTHROPIC_API_KEY"},
            {"key": "openai", "apikey": "$OPENAI_API_KEY"},
        ],
        "fields": [
            {
                "type": "string",
                "key": "apikey",
                "title": "API Key",
            }
        ],
    },
]
