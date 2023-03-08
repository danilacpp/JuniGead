from lightbulb import Plugin, command, implements, SlashCommand, SlashContext, option
from hikari import ResponseType
from miru import View, Button, ViewContext
from Core import embed as _embed

plugin = Plugin("Saper")


def generate_level(nums):
    from random import shuffle

    LOSTS = [False, False, False]
    s = [True for _ in range(nums - len(LOSTS))] + LOSTS
    shuffle(s)
    return s


class SaperButton(Button):
    def __init__(self, no, row=None):
        self.no = no
        super().__init__(label="⬜️", row=row)

    async def callback(self, ctx: ViewContext):
        embed = _embed("🎮 Сапер")
        s = self.view.level[self.no]
        if s:
            embed.description = "Верно, продолжайте в том же духе!"
            if self.view.valid + 1 == len(self.view.level) - 3:
                for i in self.view.children:
                    if hasattr(i, "no"):
                        i.label = "⬛️" if self.view.level[i.no] else "💣"
                        i.disabled = True
                embed.description = (
                    ":tada: Ого, невероятно! Вы нашли все пустые клетки!"
                )

            self.label = "⬛️"
            self.disabled = True
            self.view.valid += 1
        else:
            embed.description = f"💣 БУМ!!! Вы наткнулись на бомбу :skull:"
            for i in self.view.children:
                if hasattr(i, "no"):
                    i.label = "⬛️" if self.view.level[i.no] else "💣"
                    i.disabled = True
        if not self.view.message:
            return
        await self.view.message.edit(embed=embed, components=self.view.build())
        await ctx.defer()


class Saper(View):
    def __init__(self, author, mode=None):
        super().__init__(timeout=60)
        self.valid = 0
        POINTS = 12 if mode == "Компактный" else 15
        self.author = author
        self.level = generate_level(POINTS)
        ROW = 0
        for _ in range(POINTS):
            if POINTS == 12:
                if _ % 3 == 0:
                    ROW += 1
                self.add_item(SaperButton(_, ROW))
            else:
                self.add_item(SaperButton(_))


@plugin.command()
@option(
    "дизайн",
    required=False,
    description="Укажите здесь тип дизайна расположения кнопок.",
    choices=["Компактный", "Оригинальный (по умолчанию)"],
)
@command("сапер", 'Запустит игру "Сапер".')
@implements(SlashCommand)
async def saper(ctx: SlashContext):
    design = ctx.raw_options.get("дизайн")
    view = Saper(ctx.user.id, design)
    await ctx.interaction.create_initial_response(
        ResponseType.MESSAGE_CREATE,
        embed=_embed("🎮 Сапер", "Начинайте играть!"),
        components=view.build(),
    )
    await view.start(await ctx.interaction.fetch_initial_response())
    await view.wait()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
