import json
from uuid import uuid4 as uuid
import hashlib
import os


class UserDB:
    def __init__(self, filename):
        self.db_file = "data/" + filename

        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w'): pass

        with open(self.db_file, "r+") as f:
            if len(f.read()) == 0:
                f.write("{}")

        self.db = self.get_data()

    def get_data(self):
        with open(self.db_file, "r") as f:
            return json.loads(f.read())

    def get_db(self):
        return self.db

    def save_db(self):
        with open(self.db_file, "w") as f:
            f.write(json.dumps(self.db))
        self.db = self.get_data()

    def login_user(self, email, password):
        user = self.db.get(email)
        if user is None:
            return None

        if user["password"] == hashlib.sha256(password.encode()).hexdigest():
            self.db[email]["cookie"] = str(uuid())
            self.save_db()
            return self.db[email]["cookie"]

        return None

    def authenticate_user(self, cookie):
        for k in self.db:
            dbcookie = self.db[k]["cookie"]
            if dbcookie != "" and cookie == dbcookie:
                return self.db[k]

        return None

    def is_admin(self, email):
        user = self.db.get(email)
        if user is None:
            return False

        # TODO check userid type etc
        return user["userid"] > 90000000

    def add_user(self, email, userid, password):
        user = {
            "email": email,
            "userid": userid,
            "password": hashlib.sha256(password.encode()).hexdigest(),
            "cookie": "",
        }

        if self.db.get(email) is None:
            for k in self.db:
                if self.db[k]["userid"] == userid:
                    # print("user id already exists. skipping")
                    return False
        else:
            return False

        self.db[email] = user
        self.save_db()

        return True

    def delete_user(self, email):
        if self.db.get(email) is None:
            print("user doesnt exist")
            return False
        del self.db[email]
        self.save_db()
        return True

    def change_user_mail(self, old, new):
        user = self.db.get(old)
        if user is None:
            return False
        if self.db.get(new) is not None:
            print("account exists")
            return False

        user["email"] = new
        del self.db[old]
        self.db[new] = user
        self.save_db()
        return True
