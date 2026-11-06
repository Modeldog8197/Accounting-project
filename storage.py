"""Local accounts and one saved workspace per user. No server is needed."""

import hashlib
import hmac
import json
import re
import secrets
import sqlite3
from pathlib import Path


DEFAULT_DATABASE = Path.home() / '.wellledger' / 'wellledger.sqlite3'
PASSWORD_ROUNDS = 600_000


class Store:
    def __init__(self, path=DEFAULT_DATABASE):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not path.exists()
        self.connection = sqlite3.connect(path)
        if new_file:
            path.chmod(0o600)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.connection.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                salt BLOB NOT NULL,
                password_hash BLOB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS workspaces (
                user_id INTEGER PRIMARY KEY REFERENCES users(id),
                data TEXT NOT NULL,
                saved_at TEXT NOT NULL
            );
        ''')

    def sign_up(self, username, password):
        username = username.strip().lower()
        if not re.fullmatch(r'[a-z0-9_.-]{3,32}', username):
            raise ValueError('Use 3–32 letters, numbers, dots, underscores or hyphens for your username.')
        if not 8 <= len(password) <= 128 or not password.strip():
            raise ValueError('Use a password of 8–128 characters, not just spaces.')
        salt = secrets.token_bytes(16)
        password_hash = self.hash_password(password, salt)
        try:
            with self.connection:
                row = self.connection.execute(
                    'INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)',
                    (username, salt, password_hash))
            return row.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError('That username is already taken.') from exc

    @staticmethod
    def hash_password(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PASSWORD_ROUNDS)

    def log_in(self, username, password):
        if len(password) > 128:
            raise ValueError('Incorrect username or password.')
        row = self.connection.execute(
            'SELECT id, salt, password_hash FROM users WHERE username = ?',
            (username.strip().lower(),)).fetchone()
        # Do the same expensive hash even if the username is missing.
        salt = row[1] if row else bytes(16)
        candidate = self.hash_password(password, salt)
        if not row or not hmac.compare_digest(row[2], candidate):
            raise ValueError('Incorrect username or password.')
        return row[0]

    def save(self, user_id, data):
        with self.connection:
            self.connection.execute('''
                INSERT INTO workspaces (user_id, data, saved_at)
                VALUES (?, ?, strftime('%Y-%m-%d %H:%M:%S UTC', 'now'))
                ON CONFLICT(user_id) DO UPDATE SET
                    data = excluded.data, saved_at = excluded.saved_at
            ''', (user_id, json.dumps(data, ensure_ascii=False)))

    def load(self, user_id):
        row = self.connection.execute(
            'SELECT data, saved_at FROM workspaces WHERE user_id = ?', (user_id,)).fetchone()
        if row is None:
            return {}, None
        try:
            data = json.loads(row[0])
            if not isinstance(data, dict):
                raise ValueError
        except (ValueError, TypeError) as exc:
            raise ValueError('Saved data could not be read. Keep a backup of the database before repairing it.') from exc
        return data, row[1]

    def close(self):
        self.connection.close()
