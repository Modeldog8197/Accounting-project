"""Integration tests against a real MySQL server, not a SQLite substitute."""

import hashlib
import json
import secrets
import sqlite3
import tempfile
import unittest
from pathlib import Path

import mysql.connector

from import_sqlite import import_data
from storage import PASSWORD_ROUNDS, Store
from test_support import prepare_database


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.config = prepare_database()
        self.store = Store(self.config)

    def tearDown(self):
        self.store.close()

    def test_signup_login_validation_and_salted_hashes(self):
        user = self.store.sign_up(' Alice ', 'same-password')
        self.store.sign_up('bob', 'same-password')
        self.assertEqual(self.store.log_in('ALICE', 'same-password'), user)
        for username, password in [('alice', 'wrong'), ('missing', 'same-password'), ("' OR 1=1 --", 'same-password')]:
            with self.assertRaises(ValueError): self.store.log_in(username, password)
        for username, password in [('Alice', 'same-password'), ('a', 'long-password'), ('valid', 'short'), ('valid', '        ')]:
            with self.assertRaises(ValueError): self.store.sign_up(username, password)
        cursor = self.store.connection.cursor()
        cursor.execute('SELECT salt, password_hash FROM users')
        rows = cursor.fetchall(); cursor.close()
        self.assertNotEqual(rows[0][0], rows[1][0])
        self.assertNotEqual(rows[0][1], rows[1][1])
        self.assertEqual(len(rows[0][1]), 64)
        self.assertNotIn('same-password', str(rows))

    def test_restart_update_and_user_isolation(self):
        alice = self.store.sign_up('alice', 'alice-password')
        bob = self.store.sign_up('bob', 'bob-password')
        data = {'profile': {'name': 'Example'}, 'pages': {'care': {'plan': "A note's ₹ value; DROP TABLE users;"}}}
        self.store.save(alice, {'old': 'value'})
        self.store.save(alice, data)
        self.store.close(); self.store = Store(self.config)
        loaded, saved_at = self.store.load(alice)
        self.assertEqual(loaded, data)
        self.assertTrue(saved_at.endswith('UTC'))
        self.assertEqual(self.store.load(bob), ({}, None))
        cursor = self.store.connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM workspaces')
        self.assertEqual(cursor.fetchone()[0], 1); cursor.close()
        with self.assertRaises(mysql.connector.IntegrityError): self.store.save(-1, data)
        self.assertEqual(self.store.load(alice)[0], data)

    def test_unreadable_data_is_reported_not_replaced(self):
        user = self.store.sign_up('alice', 'alice-password')
        self.store.save(user, {'profile': {}})
        cursor = self.store.connection.cursor()
        cursor.execute('UPDATE workspaces SET data = %s WHERE user_id = %s', ('broken', user))
        self.store.connection.commit()
        with self.assertRaises(ValueError): self.store.load(user)
        cursor.execute('SELECT data FROM workspaces WHERE user_id = %s', (user,))
        self.assertEqual(cursor.fetchone()[0], 'broken'); cursor.close()

    def test_fresh_reads_and_reconnect(self):
        user = self.store.sign_up('alice', 'alice-password')
        self.store.save(user, {'profile': {'name': 'Before'}})
        other = Store(self.config)
        try:
            self.assertEqual(other.load(user)[0]['profile']['name'], 'Before')
            self.store.save(user, {'profile': {'name': 'After'}})
            self.assertEqual(other.load(user)[0]['profile']['name'], 'After')
        finally:
            other.close()
        self.store.connection.close()
        self.store.save(user, {'profile': {'name': 'Reconnected'}})
        self.assertEqual(self.store.load(user)[0]['profile']['name'], 'Reconnected')

    def test_optional_sqlite_import_preserves_credentials_and_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'old.sqlite3'
            old = sqlite3.connect(path)
            old.executescript('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, salt BLOB, password_hash BLOB);
                CREATE TABLE workspaces (user_id INTEGER PRIMARY KEY, data TEXT, saved_at TEXT);''')
            salt = secrets.token_bytes(16)
            password_hash = hashlib.pbkdf2_hmac('sha256', b'old-password', salt, PASSWORD_ROUNDS)
            data = {'profile': {'name': 'Example'}, 'reminders': {'2026-11-07': 'A note'}}
            old.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (1, 'old-user', salt, password_hash))
            old.execute('INSERT INTO workspaces VALUES (?, ?, ?)', (1, json.dumps(data), '2026-11-07 10:00:00 UTC'))
            old.commit(); old.close()
            original = path.read_bytes()
            self.assertEqual(import_data(path, self.store), 1)
            self.assertEqual(self.store.log_in('old-user', 'old-password'), 1)
            self.assertEqual(self.store.load(1)[0], data)
            self.assertEqual(path.read_bytes(), original)
            with self.assertRaises(ValueError): import_data(path, self.store)
            self.assertEqual(self.store.load(1)[0], data)


if __name__ == '__main__':
    unittest.main()
