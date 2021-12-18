#!/bin/bash
set -euo pipefail
exec java -cp ".:log4j-api-2.14.1.jar:log4j-core-2.14.1.jar" Vuln
