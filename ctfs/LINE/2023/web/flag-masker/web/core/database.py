from sqlite3 import connect
from core.config import Config


class Database:
    def __init__(self):
        try:
            self.conn = connect("./memo.db", check_same_thread=False)
            cursor = self.conn.cursor()

            with open("init.sql", "r") as fp:
              cursor.executescript(fp.read())

            self.conn.commit()

        except Exception as error:
            print(error, flush=True)

        finally:
            cursor.close()

    def write(self, data: object):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                Config.quries["write"],
                {
                    "uid": data["uid"],
                    "memo": data["memo"],
                    "secret": data["secret"]
                },
            )
            self.conn.commit()

        except Exception as error:
            print(error)

        finally:
            cursor.close()

    def loads(self, data: object):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                Config.quries["loads"],
                {
                  "uid": data["uid"],
                },
            )
            return cursor.fetchall()

        except Exception as error:
            print(error)

        finally:
            cursor.close()