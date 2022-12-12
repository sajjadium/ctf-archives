from datetime import datetime
import time
import os
import secrets
from .models import User
from .globals import Database
from .models import LoginLog
from threading import Thread
import socket
import logging
import subprocess


class LoginHelper:
    usr = None

    def _constant_time_compare(self, s1, s2):
        val = 0
        for i in range(0, len(s1)):
            val |= ord(s1[i]) ^ ord(s2[i % len(s2)])
        return val == 0

    def check_user(self, user, password, ip=None):
        log = logging.getLogger("LoginHelper.check_user")
        log.debug("Checking user %s", user)
        if user != "" and password != "":
            self.usr = User.query.filter_by(username=user).first()
            if self.usr is not None:
                # This is a secure feature, basically to prevent timing attacks, basically it will
                # take always the same amount of time to check the password
                # this way an attacker can't know if the password is correct or not
                # by checking the time it takes to check the password
                # wikipedia: https://en.wikipedia.org/wiki/Timing_attack
                if self.usr.level > 1:
                    log.info("[ADMIN_AUTH] [%s] - Trying authentication for user %s", user,
                             time.strftime("%Y-%m-%d %H:%M:%S"))
                    usr = self.usr
                    self.usr = None
                    ret = self._constant_time_compare(usr.password, usr.hash_password(password)), usr
                    if ret[0]:
                        # Log accesses for admins
                        rec = LoginLog(user, ip, datetime.utcnow(), True)
                        Database.session.add(rec)
                        Database.session.commit()
                    return ret
                else:
                    log.info("[USER_AUTH] [%s] - Trying authentication for user %s", user,
                             time.strftime("%Y-%m-%d %H:%M:%S"))
                    ret = self._constant_time_compare(self.usr.password, self.usr.hash_password(password)), self.usr
                    self.usr = None
                    return ret
        self.usr = None
        return False


class ServerHelper:

    def stop_miniserver(self, proc):
        time.sleep(600)
        # kill process
        proc.kill()

    def start_miniserver(self):
        global ServerPID, ServerPort
        if ServerPID != 0:
            # check if process is still running
            try:
                os.kill(ServerPID, 0)
            except OSError:
                # process is dead
                ServerPID = 0
            else:
                # process is alive
                return ServerPID, ServerPort, None
        # get free port
        # start miniserver
        port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port.bind(("", 0))
        port.listen(1)
        free = port.getsockname()[1]
        port.close()
        # start miniserver
        # spawn process and get pid
        # save pid and port in db
        # return pid and port
        try:
            # redirect stdout and stderr to /dev/null
            proc = subprocess.Popen(["python3", "miniserver.py", str(free)])
            thread = Thread(target=self.stop_miniserver, args=(proc,))
            thread.daemon = True
            thread.start()
            ServerPID = proc.pid
            ServerPort = free
            return proc.pid, free, None
        except Exception as e:
            return None, None, e


ServerPort = 0
ServerPID = 0
Manager = LoginHelper()
ServerManager = ServerHelper()
