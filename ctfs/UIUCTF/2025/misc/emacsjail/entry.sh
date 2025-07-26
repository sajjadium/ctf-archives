#!/bin/sh

emacs --version
emacs -nw --no-site-file --no-site-lisp --no-x-resources --no-splash --batch -l challenge.el 2>&1
