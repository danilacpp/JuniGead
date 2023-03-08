from sqlitedict import SqliteDict


class DataDriver(SqliteDict):
    def __init__(self, guild, id):
        super().__init__(
            f'./DataBase/{"Guilds" if guild else "Users"}.sqlite3', str(id)
        )

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            return None
