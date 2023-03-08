from miru import View, Button, ViewContext
from hikari import ButtonStyle
from lightbulb import Plugin, command, implements, SlashCommand, SlashContext, option
from hikari import ResponseType, MessageFlag
from Core import embed

plugin = Plugin("Maze")


def get_level(no: int):
    from random import shuffle

    chunk = [True, True, False]
    level = []
    for _ in range(no):
        _chunk = chunk.copy()
        shuffle(_chunk)
        level.append(_chunk)

    return level


class MazeButton(Button):
    def __init__(self, no):
        super().__init__(style=ButtonStyle.SUCCESS, label=str(no + 1))
        self.no = no

    async def callback(self, ctx: ViewContext):
        if not self.view.message:
            return
        if self.view.level[0][self.no]:
            self.view.level.pop(0)
            await self.view.message.edit(
                embed=embed(
                    "🎮 Лабиринт",
                    f"Правильная дверь!\nОсталось комнат: {len(self.view.level)}.",
                )
            )
        else:
            await self.view.message.edit(
                embed=embed(
                    "🎮 Лабиринт",
                    "Тупик! Конец игры.",
                ),
                components=None,
            )

        if len(self.view.level) == 0:
            await self.view.message.edit(
                embed=embed(
                    "🎮 Лабиринт",
                    ":tada: Лабиринт пройден!",
                ),
                components=None,
            )
            self.view.stop()

        await ctx.defer()


class Maze(View):
    def __init__(self, author, no):
        super().__init__()
        self.author = author
        self.level = get_level(no or 3)
        for i in range(3):
            self.add_item(MazeButton(i))


@plugin.command()
@option("комнаты", "Кол-во комнат в игре (по умолчанию 3).", required=False, type=int)
@command("лабиринт", 'Запустит игру "Лабиринт".')
@implements(SlashCommand)
async def mountain(ctx: SlashContext):
    s = ctx.raw_options.get("комнаты")
    if s and (s > 10 or s < 2):
        await ctx.respond(
            ResponseType.MESSAGE_CREATE,
            flags=MessageFlag.EPHEMERAL,
            embed=embed(
                "⚠️ Ошибка",
                'Значение параметра "комнаты" должен быть в промежутке от 2 до 10 включительно.',
            ),
        )
        return
    view = Maze(ctx.user.id, s)
    await ctx.respond(
        ResponseType.MESSAGE_CREATE,
        embed=embed(
            "🎮 Лабиринт",
            "Начинайте играть!",
        ),
        components=view.build(),
    )
    await view.start(await ctx.interaction.fetch_initial_response())
    await view.wait()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
