from lightbulb import Plugin, command, SlashCommand, SlashContext, implements
from hikari import ResponseType, MessageFlag
from miru import View, Modal, ModalContext, ViewContext, TextInput, button, Button
from Core import embed

plugin = Plugin("угадай_число")


class ModalGTN(Modal):
    number: TextInput = TextInput(
        label="Ваше число", placeholder="Пишите сюда только число.", required=True
    )

    def __init__(self, number: int, view: "GTN"):
        self._number = number
        self.view = view
        super().__init__("Угадай число")

    async def callback(self, ctx: ModalContext):
        if not self.view.message:
            return
        try:
            s: int = int(self.number.value or 0)
        except ValueError:
            await ctx.interaction.create_initial_response(
                ResponseType.MESSAGE_CREATE,
                embed=embed("⚠️ Ошибка", " Введите число!"),
                flags=MessageFlag.EPHEMERAL,
            )
            return

        if s < self._number or s > self._number:
            await self.view.message.edit(
                embed=embed(
                    "🎮 Угадай число",
                    "  Мое число "
                    + ("больше чем ваше." if s < self._number else "меньше чем ваше."),
                )
            )
        else:
            await self.view.message.edit(
                embed=embed(
                    "🎮 Угадай число",
                    f":tada: Вы угадали! Число - {s}.",
                ),
                components=None,
            )
            self.view.stop()

        await ctx.defer()


class GTN(View):
    def __init__(self, author):
        import random

        self.number = random.randint(0, 200)
        self.author = author
        super().__init__()

    @button(label="Сказать число")
    async def call(self, button: Button, ctx: ViewContext):
        modal = ModalGTN(self.number, self)
        await ctx.respond_with_modal(modal)


@plugin.command()
@command("угадай_число", 'Запустит игру "Угадай число".')
@implements(SlashCommand)
async def gtn(ctx: SlashContext):
    view = GTN(ctx.user.id)
    await ctx.respond(
        embed=embed(
            "🎮 Угадай число",
            "Начинайте! Я загадал число в диапазоне от 0 до 200.",
        ),
        components=view.build(),
    )
    await view.start(await ctx.interaction.fetch_initial_response())
    await view.wait()


def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)
