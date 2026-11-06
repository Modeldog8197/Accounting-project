"""Account validation, password storage and restart persistence without a GUI."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from storage import Store


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'data' / 'test.sqlite3'
        self.store = Store(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_signup_login_validation_and_salted_hashes(self):
        user = self.store.sign_up(' Alice ', 'same-password')
        self.store.sign_up('bob', 'same-password')
        self.assertEqual(self.store.log_in('ALICE', 'same-password'), user)
        for username, password in [('alice', 'wrong'), ('missing', 'same-password'), ("' OR 1=1 --", 'same-password')]:
            with self.assertRaises(ValueError): self.store.log_in(username, password)
        for username, password in [('Alice', 'same-password'), ('a', 'long-password'), ('valid', 'short'), ('valid', '        ')]:
            with self.assertRaises(ValueError): self.store.sign_up(username, password)
        rows = self.store.connection.execute('SELECT salt, password_hash FROM users').fetchall()
        self.assertNotEqual(rows[0][0], rows[1][0])
        self.assertNotEqual(rows[0][1], rows[1][1])
        self.assertNotIn(b'same-password', self.path.read_bytes())

    def test_restart_overwrite_and_user_isolation(self):
        alice = self.store.sign_up('alice', 'alice-password')
        bob = self.store.sign_up('bob', 'bob-password')
        data = {'profile': {'name': 'Example'}, 'pages': {'care': {'plan': "A note's ₹ value"}}}
        self.store.save(alice, {'old': 'value'})
        self.store.save(alice, data)
        self.store.close(); self.store = Store(self.path)
        loaded, saved_at = self.store.load(alice)
        self.assertEqual(loaded, data)
        self.assertTrue(saved_at.endswith('UTC'))
        self.assertEqual(self.store.load(bob), ({}, None))
        self.assertEqual(self.store.connection.execute('SELECT count(*) FROM workspaces').fetchone()[0], 1)
        with self.assertRaises(sqlite3.IntegrityError): self.store.save(9999, data)

    def test_unreadable_data_is_reported_not_replaced(self):
        user = self.store.sign_up('alice', 'alice-password')
        self.store.save(user, {'profile': {}})
        self.store.connection.execute("UPDATE workspaces SET data = 'broken'")
        with self.assertRaises(ValueError): self.store.load(user)
        self.assertEqual(self.store.connection.execute('SELECT data FROM workspaces').fetchone()[0], 'broken')


if __name__ == '__main__':
    unittest.main()
