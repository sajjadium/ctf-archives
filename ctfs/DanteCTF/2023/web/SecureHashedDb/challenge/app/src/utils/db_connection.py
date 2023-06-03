import os
import re


class db_Connection(object):

    def __init__(self, app, mysql, utils) -> None:
        self.app = app
        self.mysql = mysql
        self.utils = utils
        # MySQL configurations
        self.app.config['MYSQL_USER'] = os.getenv('MYSQL_DATABASE_USER')
        self.app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
        self.app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE_DB')
        self.app.config['MYSQL_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
        self.app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

        self.mysql.init_app(self.app)

    def initMySql(self):
        return self.mysql.connection.cursor()

    def __recursiveStrip(self, query):
        # Copied from stack overflow, I don't even know what it filters exactly
        matches = ["updatexml", "extract", "%", "unhex", "hex",
                   "join", "roles", "id", "rolestring", "role",
                   "ascii", "concat", "lower", "upper", "mid", "substr", "substring",
                   "replace", "right", "left", "strcmp", "rtrim", "rpad", "ucase", "lcase",
                   "max", "cast", "conv", "convert", "if", "benchmark", ">", "<",
                   "->", "/", "*", "aes", "char", "compress", "find", "base64", "instr",
                   "is", "json", "left", "md5", "oct", "ord", "regexp", "sha", "space", "digest",
                   "trim", "uncompress", "xor", "~", "|", "case", "when"]

        patterns = [".*,.*[uU][sS][eE][rR][nN][aA][mM][eE]"]

        for x in patterns:
            if re.match(x, query.lower()):
                query = query.lower()
                query = re.sub(x, "", query)

        for x in matches:
            if x in query.lower():
                query = query.lower()
                query = query.replace(x, "")

        return self.__recursiveStrip(query) \
            if any([x in query.lower() for x in matches]) \
            or any([re.match(query.lower(), x) for x in patterns]) \
            else query

    def staticAdminSelector(self, cursor):
        cursor.execute(f"SELECT username FROM user as u JOIN roles as r ON u.id = r.id WHERE r.roleString = 'admin'")
        got = cursor.fetchall()

        return got[0]['username'] if len(got) > 0 else self.utils.generateRandomToken(20)

    def queryExecutor(self, query, cursor):

        query = query.replace("'", "\\'")
        matches = ["select", "where", "sleep"]

        # Adding some personal filters just to be 100% sure

        if any([x in query.lower() for x in matches]):
            query = re.sub("[Ss][Ee][Ll][Ee][Cc][Tt]", "", query)
            query = re.sub("[Ww][Hh][Ee][Rr][Ee]", "", query)
            query = re.sub("[Ss][Ll][Ee][Ee][Pp]", "", query)

        escaped = self.__recursiveStrip(query)

        thrownException = False
        got = []

        try:
            cursor.execute(f"SELECT * FROM user WHERE username = '{escaped}'")
            got = cursor.fetchall()
        except:
            thrownException = True

        return got[0] if not thrownException and len(got) > 0 else None
