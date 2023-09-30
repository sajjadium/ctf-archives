pnpm start & > next-site-log 2>&1
python3 -m http.server 8080 -d flag & > python-flag-log 2>&1

tail -f /dev/null
