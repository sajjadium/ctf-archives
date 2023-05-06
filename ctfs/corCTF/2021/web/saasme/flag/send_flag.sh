while [ true ]
do
  curl -G "http://chall:8000/flag" --data-urlencode "flag=$FLAG"
  sleep 15
done