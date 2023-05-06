mv /home/pwn/spawner /
chown root:root /spawner
chmod 750 /spawner

sed -i 's$%sarg%$-w 224,27,20 -u -r -p -n -c /home/pwn -t 3 -o 16 -f 6 /pwn$g' /home/pwn/xinetd # PoW enabled(-w), timeout 3s. 
sed -i 's$%server%$/spawner$g' /home/pwn/xinetd
mv /home/pwn/xinetd /etc/xinetd.d/xinetd
mv /home/pwn/xinetd.conf /etc/
mv /home/pwn/boot.sh /
cd /home/pwn
mkdir lib64
mkdir lib
mkdir bin
chown -R root:root /home/pwn
chmod -R 755 /home/pwn
echo 'xinetd error. CPS limit reached?' > /etc/banner_fail
