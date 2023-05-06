java -Xms32m -Xmx32m -jar app.jar # &
# while true; do wget http://localhost:10000/bin/create --post-data="bin=$FLAG" -S 2>&1 | grep -i location; sleep 10; done;