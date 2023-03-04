from lightbulb import Plugin, command, implements, SlashCommand, SlashContext, option
from Core import embed, send_doc_command

plugin = Plugin("Help_Module")


@plugin.command()
@option("команда", "Покажет справку по выбранной команде.", required=False)
@command("хелп", "Покажет справку.")
@implements(SlashCommand)
async def help_command(ctx: SlashContext):
    command = ctx.bot.slash_commands.get(ctx.raw_options.get("команда"))
    if command:
        await ctx.respond(embed=embed("Справка", send_doc_command(command)))
    else:
        await ctx.respond(
            embed=embed(
                "Справка",
                "Добро пожаловать в справочную систему JuniGead!\n\n"
                "Справочные команды: /хелп\n",
            ).set_footer(
                "Вы также сможете посмотреть справку отдельной команды: /хелп команда"
            )
        )


def load(bot) -> None:
    bot.add_plugin(plugin)


def unload(bot) -> None:
    bot.remove_plugin(plugin)
