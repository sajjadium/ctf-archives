#!/usr/bin/env python3

with open("sqlite_web/sqlite_web.py", "r") as f:
    orig = f.read()

patched = orig.replace("""'SELECT *\\nFROM "%s"'""", '''"""WITH bytes(i, s) AS (
    VALUES(1, '') UNION ALL
    SELECT i + 1, (
        SELECT ((v|k)-(v&k)) & 255 FROM (
            SELECT
                (SELECT asciicode from ascii where hexcode = hex(SUBSTR(sha512('hxp{REDACTED}'), i, 1))) as k,
                (SELECT asciicode from ascii where hexcode = hex(SUBSTR(encrypted, i, 1))) as v
            FROM %s
        )
    ) AS c FROM bytes WHERE c <> '' limit 64 offset 1
) SELECT group_concat(char(s),'') FROM bytes;"""''')

with open("sqlite_web/sqlite_web.py", "w") as f:
    f.write(patched)