#!/bin/bash
sed -ue '/^\./ { /^\.open/!d; }' | /jailed/sqlite3 -interactive