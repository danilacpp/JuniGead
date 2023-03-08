"""
(c) 2023 danilacpp | Проект JuniGead
"""
import os
from lightbulb import BotApp
from hikari import Activity
from miru import install
from Core import DataDriver

if os.name != "nt":
    import uvloop

    uvloop.install()

db = DataDriver(False, -1)
app = BotApp(os.environ.get("TOKEN") or open("./token.txt").read())
app.d.commands = 0
app.d._commands = db["commands"] or 0

app.load_extensions_from("./Modules")

install(app)
app.run(activity=Activity(name="https://junigead.ru"))

db["commands"] = db["commands"] or 0 + app.d.commands
db.commit()
db.close()
