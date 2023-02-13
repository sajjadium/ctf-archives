while !</dev/tcp/db/5432
  do sleep 1
done
node /app/flagserver.js