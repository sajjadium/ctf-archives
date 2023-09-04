from crypto import g, p, Messenger
from secrets import randbelow
import os


class Bots:
    def __init__(self, db):
        self.db = db

    def setup(self):
        self.admin_privkey = randbelow(p)
        self.flag_haver_privkey = randbelow(p)

        self.admin_pubkey = pow(g, self.admin_privkey, p)
        self.flag_haver_pubkey = pow(g, self.flag_haver_privkey, p)

        self.db.add_user('admin', self.admin_pubkey)
        self.db.add_user('flag_haver', self.flag_haver_pubkey)

    def send_welcome_message(self, target_user):
        target_user_pubkey = self.db.get_user_pubkey(target_user)
        msg_enc, sig = Messenger(self.admin_privkey).send(target_user_pubkey, f'Welcome {target_user}!'.encode())
        self.db.add_message('admin', target_user, msg_enc, sig)

    def receive_flag_message(self, msg):
        sender, _, msg_enc, sig = msg
        sender_pubkey = self.db.get_user_pubkey(sender)
        msg = Messenger(self.flag_haver_privkey).receive(sender_pubkey, msg_enc, sig)
        if not msg or sender != 'admin':
            return
        if msg.startswith(b'Send flag to '):
            user = msg[13:].decode()
            if not self.db.user_exists(user):
                return
            user_pubkey = self.db.get_user_pubkey(user)
            FLAG = open(os.path.join(os.path.dirname(__file__), 'flag.txt'), 'r').read()
            msg_enc, sig = Messenger(self.flag_haver_privkey).send(user_pubkey, f'Here is the flag: {FLAG}'.encode())
            self.db.add_message('flag_haver', user, msg_enc, sig)

    def perform_bot_user_actions(self):
        for user in self.db.users:
            if user not in ['flag_haver', 'admin'] and len(self.db.get_inbox(user)) == 0:
                self.send_welcome_message(user)

        for msg in self.db.get_inbox('flag_haver'):
            self.receive_flag_message(msg)

        self.db.clear_inbox('flag_haver')
