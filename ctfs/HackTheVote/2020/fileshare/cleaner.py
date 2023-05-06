import os, time, shutil

def get_used_dirs():
    pids = [p for p in os.listdir("/proc") if p.isnumeric()]
    res = set()
    for p in pids:
        try:
            path = os.path.realpath("/proc/%s/cwd"%p)
            if path.startswith("/tmp/fileshare."):
                res.add(path)
        except:
            pass
    return res

while True:
    try:
        dirs = ["/tmp/"+d for d in os.listdir("/tmp") if d.startswith("fileshare.")]
        used = get_used_dirs()
        for d in dirs:
            if d not in used:
                try:
                    os.system("umount %s/proc"%d)
                    shutil.rmtree(d)
                except:
                    pass
    except:
        pass
    time.sleep(5)
