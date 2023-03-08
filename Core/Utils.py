from hikari import Embed, Color
from lightbulb import SlashCommand


def embed(title: str, description=None) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=Color.from_hex_code("#FF0000")
        if title == "Ошибка"
        else Color.from_hex_code("#6c92af"),
    )


def send_doc_command(command: SlashCommand) -> str:
    REQUIRED_OPTIONS = []
    NOT_REQUIRED_OPTIONS = []
    DOCSTRING = f"{command.description}\n\nСинтаксис:\n\n```/{command.name} "
    if len(command.options) != 0:
        for option in command.options.values():
            if option.required:
                REQUIRED_OPTIONS.append(option)
            else:
                NOT_REQUIRED_OPTIONS.append(option)

        if len(REQUIRED_OPTIONS) != 0:
            for option in REQUIRED_OPTIONS:
                DOCSTRING += f"<{option.name}> "

        if len(NOT_REQUIRED_OPTIONS) != 0:
            for option in NOT_REQUIRED_OPTIONS:
                DOCSTRING += f"[{option.name}] "

        DOCSTRING += "```\n\n<> - обязательная опция, [] - необязательная опция"

        return DOCSTRING


# Константы

DOT = "<:dot:1004787588751699978>"
__version__ = "2023.4.0 (Бесплатная серия)"
