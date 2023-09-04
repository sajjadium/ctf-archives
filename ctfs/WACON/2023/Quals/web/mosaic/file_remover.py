import os, time
from threading import Thread

def flag_remover():
    while True:
        try:
            time.sleep(3)
            os.system("rm -rf /app/uploads/admin/*")
            os.system("rm -rf /app/static/uploads/admin/*")
        except:
            continue

def userfile_remover():
    while True:
        try:
            time.sleep(600)
            os.system("rm -rf /app/uploads/*/*")
            os.system("rm -rf /app/static/uploads/*/*")
        except:
            continue

th1 = Thread(target=flag_remover)
th2 = Thread(target=userfile_remover)
th1.start()
th2.start()
