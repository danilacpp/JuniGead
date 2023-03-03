"""
JuniGead discord bot.
(c) 2023 danilacpp
"""
import os
from lightbulb import BotApp
from hikari import Activity

if os.name != "nt":
    import uvloop
    uvloop.install()

app = BotApp(
    os.environ.get("TOKEN") or open("./token.txt").read()
)

app.run(
    activity=Activity(
        name="https://junigead.ru"
    )
)
