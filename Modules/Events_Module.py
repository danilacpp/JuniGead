from lightbulb import Plugin
from hikari import (
    InteractionCreateEvent,
    CommandInteraction,
    ComponentInteraction,
    ResponseType,
    MessageFlag,
)
from miru.view import get_view
from Core import embed

plugin = Plugin("Events")


@plugin.listener(InteractionCreateEvent)
async def on_interaction(event: InteractionCreateEvent):
    if isinstance(event.interaction, CommandInteraction):
        plugin.bot.d.commands += 1
    else:
        if isinstance(event.interaction, ComponentInteraction):
            view = get_view(event.interaction.message.id)
            if not view:
                await event.interaction.create_initial_response(
                    ResponseType.MESSAGE_CREATE,
                    embed=embed(
                        "⚠️ Ошибка",
                        "У данного взаимодействия истек срок действия. "
                        "Введите связанную с ним команду повторно в случае, если это необходимо.",
                    ),
                    flags=MessageFlag.EPHEMERAL,
                )
            else:
                author = view.__getattribute__("author") or event.interaction.user.id
                if author != event.interaction.user.id:
                    await event.interaction.create_initial_response(
                        ResponseType.MESSAGE_CREATE,
                        embed=embed(
                            "⚠️ Ошибка", "Данное взаимодействие адресовано не вам."
                        ),
                        flags=MessageFlag.EPHEMERAL,
                    )


def load(bot) -> None:
    bot.add_plugin(plugin)


def unload(bot) -> None:
    bot.remove_plugin(plugin)
