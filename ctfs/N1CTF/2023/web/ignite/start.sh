/flag.sh
export FLAG=not_flag
while true; do
    su - ctf -c "export JAVA_HOME=/opt/java/openjdk && export FLAG=not_flag && export IGNITE_HOME=/opt/ignite/apache-ignite && /bin/sh -c $IGNITE_HOME/run.sh"
    sleep 1
done