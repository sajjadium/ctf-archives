#!/bin/bash
set -euo pipefail
echo 'Submit JavaScript code, end with EOF'
exec njs -s -u - 2>&1
