mv /home/pwn/spawner /
chown root:root /spawner
chmod 750 /spawner

sed -i 's$%sarg%$-w 224,27,20 -r -c /home/pwn /runner$g' /home/pwn/xinetd # # PoW enabled(-w)
sed -i 's$%server%$/spawner$g' /home/pwn/xinetd
mv /home/pwn/xinetd /etc/xinetd.d/xinetd
mv /home/pwn/xinetd.conf /etc/
mv /home/pwn/boot.sh /
cd /home/pwn
chown -R root:root /home/pwn
chmod -R 755 /home/pwn
chmod 511 /home/pwn/readflag
echo 'xinetd error. CPS limit reached?' > /etc/banner_fail
