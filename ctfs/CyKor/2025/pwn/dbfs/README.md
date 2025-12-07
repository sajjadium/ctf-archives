the database in the filesystem!

Note: If you are using AppArmor, nsjail may not work properly. To disable AppArmor restrictions temporarily, run these commands:

sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
