#!/bin/sh

VULN="${1:-./vuln}"

ncat -l 127.0.0.1 1337 -c "${VULN}" &
