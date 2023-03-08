from lightbulb import Plugin, command, implements, SlashCommand, SlashContext
from Core import embed, DOT, __version__

plugin = Plugin("Stat")


@plugin.command()
@command("стат", "Покажет стаистику JuniGead: кол-во серверов, пользователей и т.д.")
@implements(SlashCommand)
async def help_command(ctx: SlashContext):
    commands = (plugin.app.d.commands + 1, plugin.app.d._commands)
    await ctx.respond(
        embed=embed("Статистика JuniGead")
        .add_field(
            "Основная",
            f"{DOT} Серверов: {len(ctx.bot.cache.get_available_guilds_view())}\n"
            f"{DOT} Пользователей: {len(ctx.bot.cache.get_users_view())}\n",
            inline=True,
        )
        .add_field(
            "Платформа",
            f"{DOT} Пинг: {int(ctx.bot.heartbeat_latency * 1000)} мс\n"
            f"{DOT} Обработано команд (Всего/С момента запуска): {sum(commands)}/{commands[0]}\n"
            f"{DOT} Сборка: [{__version__}](https://github.com/danilacpp/JuniGead)",
            inline=True,
        )
    )


def load(bot) -> None:
    bot.add_plugin(plugin)


def unload(bot) -> None:
    bot.remove_plugin(plugin)
