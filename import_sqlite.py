"""Optional one-time copy of the old SQLite data into an empty MySQL database."""

import argparse
import sqlite3
from pathlib import Path

from storage import Store


def import_data(source_path, store):
    path = Path(source_path).expanduser().resolve()
    if not path.is_file():
        raise ValueError('The SQLite file does not exist.')
    source = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
    cursor = store.open_cursor()
    try:
        cursor.execute('SELECT id FROM users')
        if cursor.fetchall():
            raise ValueError('Import needs an empty MySQL database. Existing accounts will not be overwritten.')
        users = source.execute('SELECT id, username, salt, password_hash FROM users').fetchall()
        workspaces = source.execute('SELECT user_id, data, saved_at FROM workspaces').fetchall()
        for user_id, username, salt, password_hash in users:
            cursor.execute(
                'INSERT INTO users (id, username, salt, password_hash) VALUES (%s, %s, %s, %s)',
                (user_id, username, salt.hex(), password_hash.hex()))
        for user_id, data, saved_at in workspaces:
            cursor.execute(
                'INSERT INTO workspaces (user_id, data, saved_at) VALUES (%s, %s, %s)',
                (user_id, data, saved_at))
        store.connection.commit()
        return len(users)
    except Exception:
        store.connection.rollback()
        raise
    finally:
        cursor.close()
        source.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', nargs='?', default=str(Path.home() / '.wellledger' / 'wellledger.sqlite3'))
    args = parser.parse_args()
    database = Store()
    try:
        count = import_data(args.source, database)
        print(f'Imported {count} accounts. Your original SQLite file was not changed.')
    finally:
        database.close()
