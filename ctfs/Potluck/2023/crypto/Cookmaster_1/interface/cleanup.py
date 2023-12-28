#!/usr/bin/env python3
import sqlite3
import time
import os
from src.container import container_state


DB_PATH=os.environ.get('DB_PATH', '/data/team_info.db')


if __name__ == '__main__':
    while True:
        try:
            con = sqlite3.connect(DB_PATH)
            print('Cleaning instances')
            cursor = con.execute('SELECT instance_id FROM instances WHERE valid_until < strftime("%s", "now")')
            instance_ids = [(row[0],) for row in cursor.fetchall()]
            print(f'Cleaning up {len(instance_ids)} instances')
            for (iid,) in instance_ids:
                container_state(iid, 'stop')
            cursor.executemany('DELETE FROM instances WHERE instance_id = ?', instance_ids)
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(e)

        print('Sleeping')
        time.sleep(10)
