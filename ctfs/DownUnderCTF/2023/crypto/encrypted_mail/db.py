from collections import defaultdict
from time import time


class Database:
    def __init__(self):
        self.users = {}
        self.inboxes = defaultdict(list)
        self.current_user = None

    def add_user(self, username, pubkey):
        self.users[username] = pubkey

    def user_exists(self, username):
        return username in self.users

    def get_user_pubkey(self, username):
        return self.users[username]

    def set_current_user(self, username):
        self.current_user = username

    def get_current_user(self):
        return self.current_user

    def get_inbox(self, username):
        return self.inboxes[username]

    def clear_inbox(self, username):
        self.inboxes[username] = []

    def add_message(self, sender, recipient, msg_enc, sig):
        self.inboxes[recipient].append((sender, int(time()), msg_enc, sig))
