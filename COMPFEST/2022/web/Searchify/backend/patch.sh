#!/bin/sh
find /usr/local/lib/python3.10/site-packages -type f -name '__init__.py' | xargs -Iz sh -c 'sed -Ei "s/(> .0):/\1 and 0:/g" z'