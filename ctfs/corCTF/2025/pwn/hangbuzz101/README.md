FizzBuzz101
While other VR firms find real 0-days, we only find random "hangs"!

Hint: Take a look at net/sched and tc

Note that the kernel is built with the config below at commit of: 8742b2d8935f

We patch it with the following command:

sed -i "s/BUG: soft lockup/BUG: soft lockup, here is your flag: ${FLAG}/g" kernel/watchdog.c
