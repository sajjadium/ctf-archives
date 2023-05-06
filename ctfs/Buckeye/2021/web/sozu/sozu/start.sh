#!/bin/bash

APP_IP=$(getent hosts app | awk '{ print $1 }')

mkdir /etc/sozu/
cat <<EOF > /etc/sozu/config.toml
[[listeners]]
protocol = "http"
address = "0.0.0.0:3000"

[applications]

[applications.NameOfYourApp]
protocol = "http"
frontends = [
  { address = "0.0.0.0:3000", hostname = "$HOSTNAME", path_begin = "/public"  },
]

backends  = [
  { address = "$APP_IP:8000"  }
  
]
EOF

/sozu start -c /etc/sozu/config.toml
