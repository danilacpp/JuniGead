from random import randint, shuffle
from lightbulb import Plugin, command, implements, SlashCommand, SlashContext, option
from hikari import ResponseType, MessageFlag, ButtonStyle
from miru import button, ViewContext, View, Button
from Core import embed

plugin = Plugin("Mountain")


def get_level(rooms: int = 3):
    level = []
    chunk = [0, 1, 1]
    for _ in range(rooms):
        _chunk = chunk.copy()
        if randint(0, 2) == 2:
            _chunk.pop(randint(1, 2))
            _chunk.append(2)

        shuffle(_chunk)
        shuffle(_chunk)
        level.append(_chunk)
        del _chunk

    return level


class Mountain(View):
    def __init__(self, author: int, rooms: int):
        super().__init__()
        self.author = author
        self.level = get_level(rooms)
        self.hp = 100

    async def on(self, kletka: int, warmishka: bool = False, dont_war: bool = False):
        if not warmishka and not dont_war:
            if self.level[0][kletka] == 2:
                self.door_three.disabled = True
                self.door_two.disabled = True
                self.i_hot_alone.disabled = False
                self.i_damage.disabled = False
                self.door_one.disabled = True
                await self.message.edit(
                    embed=embed(
                        "🎮 Восхождение",
                        "Вы встретили мишку! Что теперь делать будем?",
                    ),
                    components=self.build(),
                )
            elif self.level[0][kletka] == 0:
                self.level.pop(0)
                await self.message.edit(
                    embed=embed(
                        "🎮 Восхождение",
                        f"Преодолевая испытания на пути, вы вышли на вершину выше, осталось подъемов: {len(self.level)}",
                    )
                )
            else:
                for i in self.children:
                    i.disabled = True

                await self.message.edit(
                    embed=embed(
                        "🎮 Восхождение",
                        "Преодолевая испытания на пути, вы наткнулись на тупик!",
                    ),
                    components=self.build(),
                )
                self.stop()
        else:
            veroytnost = randint(0, 15 if dont_war else 10)
            if 5 < veroytnost < 7:
                minus_hp = randint(15 if warmishka else 1, 30 if warmishka else 15)
                self.hp -= minus_hp
                await self.message.edit(
                    embed=embed(
                        "🎮 Восхождение",
                        f"Блин, а ловко ты это мишка придумал, я еще в самом начале ни черта не понял, минус {minus_hp} :heart:, осталось хп: {self.hp} :heart:"
                        if warmishka
                        else f"Убежать не вышло, мишка вас догнал и вы получили урон в размере {minus_hp} :heart:, осталось хп: {self.hp} :heart:",
                    )
                )
            else:
                self.door_one.disabled = False
                self.door_three.disabled = False
                self.door_two.disabled = False
                self.i_hot_alone.disabled = True
                self.i_damage.disabled = True
                await self.message.edit(
                    embed=embed(
                        "🎮 Восхождение",
                        "Мишка миновал, можно идти дальше.",
                    ),
                    components=self.build(),
                )
                self.level.pop(0)

        await self.checkers()

    async def checkers(self):
        if self.hp <= 0 or len(self.level) == 0:
            for i in self.children:
                i.disabled = True
            await self.message.edit(
                embed=embed(
                    "🎮 Восхождение",
                    "Вы не смогли дойти до вершины, т.к у вас закончились жизни!"
                    if self.hp <= 0
                    else "Вы дошли до вершины и разместили там флаг!",
                ),
                components=self.build(),
            )
            self.stop()

    @button(label="Влево", row=1)
    async def door_one(self, button: Button, ctx: ViewContext):
        await ctx.defer()
        await self.on(0)

    @button(label="Прямо", row=1)
    async def door_two(self, button: Button, ctx: ViewContext):
        await ctx.defer()
        await self.on(1)

    @button(label="Направо", row=1)
    async def door_three(self, button: Button, ctx: ViewContext):
        await ctx.defer()
        await self.on(2)

    @button(label="Пытаться убежать", style=ButtonStyle.PRIMARY, row=2, disabled=True)
    async def i_hot_alone(self, button: Button, ctx: ViewContext):
        await ctx.defer()
        await self.on(0, i_goto_alone=True)

    @button(label="Ударить мишку", style=ButtonStyle.DANGER, row=2, disabled=True)
    async def i_damage(self, button: Button, ctx: ViewContext):
        await ctx.defer()
        await self.on(0, warmishka=True)


@plugin.command()
@option("уровни", "Кол-во комнат в игре (по умолчанию 3).", required=False, type=int)
@command("восхождение", 'Запустит игру "Восхождение".')
@implements(SlashCommand)
async def mountain(ctx: SlashContext):
    s = ctx.raw_options.get("уровни")
    if s and (s > 10 or s < 2):
        await ctx.interaction.create_initial_response(
            ResponseType.MESSAGE_CREATE,
            flags=MessageFlag.EPHEMERAL,
            embed=embed(
                "⚠️ Ошибка",
                'Значение параметра "уровни" должен быть в промежутке от 2 до 10 включительно.',
            ),
        )
        return
    view = Mountain(ctx.user.id, s or 3)
    await ctx.interaction.create_initial_response(
        ResponseType.MESSAGE_CREATE,
        embed=embed(
            "🎮 Восхождение",
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
