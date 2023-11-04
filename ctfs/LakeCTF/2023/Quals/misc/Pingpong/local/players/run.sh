#!/bin/bash
set -ex
rm -f /tmp/pids
bash -- players/4400.sh &
bash -- players/4401.sh &
A=$!
bash -- players/4444.sh &
bash -- players/4445.sh &
bash -- players/4446.sh &
bash -- players/4447.sh &
bash -- players/4448.sh &
bash -- players/4449.sh &
bash -- players/4450.sh &
bash -- players/4451.sh &
bash -- players/4452.sh &
bash -- players/4453.sh &
bash -- players/4454.sh &
bash -- players/4455.sh &
bash -- players/4456.sh &
bash -- players/4457.sh &
bash -- players/4458.sh &
bash -- players/4459.sh &
bash -- players/4460.sh &
bash -- players/4461.sh &
bash -- players/4462.sh &
bash -- players/4463.sh &
bash -- players/4464.sh &
bash -- players/4465.sh &
bash -- players/4466.sh &
bash -- players/4467.sh &
bash -- players/4468.sh &
bash -- players/4469.sh &
bash -- players/4470.sh &
bash -- players/4471.sh &
bash -- players/4472.sh &
bash -- players/4473.sh &
bash -- players/4474.sh &
bash -- players/4475.sh &
bash -- players/4476.sh &
bash -- players/4477.sh &
bash -- players/4478.sh &
bash -- players/4479.sh &
bash -- players/4480.sh &
bash -- players/4481.sh &
sleep 1
bash players/EPFL.sh &
echo "$$" > /tmp/pids
wait $A