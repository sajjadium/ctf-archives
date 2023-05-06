#!/bin/bash

BASEDIR=$(dirname "$0")
TEMP=$(mktemp -d /tmp/dtc.XXXXXXXXXXXX)
timeout -s KILL 60 ${BASEDIR}/dtc "${TEMP}" 2>/dev/null
rm -fr "${TEMP}"
