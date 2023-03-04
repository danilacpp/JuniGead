"""
(c) 2023 danilacpp | Проект JuniGead
"""
import os
from lightbulb import BotApp
from hikari import Activity

if os.name != "nt":
    import uvloop

    uvloop.install()

app = BotApp(os.environ.get("TOKEN") or open("./token.txt").read())

app.load_extensions_from("./Modules")

app.run(activity=Activity(name="https://junigead.ru"))
