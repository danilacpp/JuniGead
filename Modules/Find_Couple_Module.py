from random import shuffle
from lightbulb import Plugin, option, command, SlashCommand, SlashContext, implements
from hikari import ButtonStyle, MessageFlag
from miru import View, Button, ViewContext
from Core import embed

plugin = Plugin("Find_Couple")


def get_level(mode):
    if mode == "PC":
        s = ["🍔", "🌭", "🥨", "🥢", "🥖", "🌰", "🍔", "🌭", "🥨", "🥢", "🥖", "🌰", "🍓", "🍓"]
    else:
        s = ["🍔", "🌭", "🥨", "🥢", "🥖", "🍔", "🌭", "🥨", "🥢", "🥖", "🍓", "🍓"]

    shuffle(s)
    return s


class FindCoupleButton(Button):
    def __init__(self, no, row):
        self.no = no
        super().__init__(label=f"{no}", row=row, style=ButtonStyle.PRIMARY)

    async def callback(self, ctx: ViewContext):
        if not self.view.message:
            return
        self.label = self.view.level[self.no - 1]
        if not self.view.last_button:
            self.view.last_button = self
            await self.view.message.edit(
                embed=embed("🎮 Найди пару", "А теперь кликните на другую ячейку."),
                flags=MessageFlag.EPHEMERAL,
                components=self.view.build(),
            )
        elif (
            self.view.last_button.no != self.no
            and self.view.last_button.label == self.label
        ):
            self.disabled = True
            self.view.last_button.disabled = True
            if self.view.last_button:
                self.view.last_button = None
            await self.view.message.edit(
                components=self.view.build(),
                embed=embed(
                    "🎮 Найди пару",
                    "Ура, совпадение! Ячейки открыты.",
                ),
            )
            if all(i.disabled for i in self.view.children):
                await self.view.message.edit(
                    components=None,
                    embed=embed("🎮 Найди пару", "Все пары открыты! Спасибо за игру."),
                )
                self.view.stop()
        elif (
            self.view.last_button.no == self.no
            and self.view.last_button.label == self.label
        ):
            await ctx.respond(
                embed(
                    "⚠️ Ошибка",
                    "Ух ты! Нельзя одно и тоже выбирать. Может, выбрать что-то другое?",
                ),
                flags=MessageFlag.EPHEMERAL,
            )
            return
        else:
            self.view.last_button.label = str(self.view.last_button.no)
            self.label = str(self.no)
            await self.view.message.edit(
                embed=embed(
                    "🎮 Найди пару",
                    f" Нет совпадения.\n"
                    f"Ваша пара: {self.view.level[int(self.view.last_button.label) - 1]} ({self.view.last_button.no}) - {self.view.level[int(self.label) - 1]} ({self.no})",
                ),
                flags=MessageFlag.EPHEMERAL,
                components=self.view.build(),
            )
            if self.view.last_button:
                self.view.last_button = None

        await ctx.defer()


class FindCouple(View):
    def __init__(self, author, mode):
        self.author = author
        self.last_button = None
        self.level = get_level(mode)
        row = 0
        super().__init__(timeout=180)
        _s = 15 if mode == "PC" else 12
        _l = 5 if mode == "PC" else 3
        for i in range(_s):
            if i % _l == 0:
                row += 1

            b = FindCoupleButton(i + 1, row)
            if i == 14:
                s = Button(label="❌", disabled=True, row=row, style=ButtonStyle.DANGER)
                self.add_item(s)
                return

            self.add_item(b)


@plugin.command()
@option(
    "дизайн",
    required=False,
    description="Укажите здесь тип дизайна расположения кнопок.",
    choices=["Компактный", "Оригинальный (по умолчанию)"],
)
@command("найди_пару", 'Запустит игру "Найди пару".')
@implements(SlashCommand)
async def help(ctx: SlashContext):
    view = FindCouple(
        ctx.author.id,
        "PC"
        if not ctx.raw_options.get("дизайн")
        or ctx.raw_options.get("дизайн") == "Оригинальный (по умолчанию)"
        else "Mobile",
    )
    await ctx.respond(
        embed=embed("🎮 Найди пару", "Начинайте играть!"),
        components=view.build(),
    )
    await view.start(await ctx.interaction.fetch_initial_response())
    await view.wait()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
