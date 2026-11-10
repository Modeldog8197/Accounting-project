"""MySQL accounts and saved inputs."""

import hashlib
import hmac
import json
import re
import secrets
from datetime import datetime, timezone

import mysql.connector


PASSWORD_ROUNDS = 600_000


def database_config():
    try:
        from db_config import DB_CONFIG
    except ImportError as exc:
        raise ValueError('Copy db_config.example.py to db_config.py and enter your MySQL details. See README.md.') from exc
    return dict(DB_CONFIG)


class Store:
    def __init__(self, config=None):
        settings = database_config() if config is None else dict(config)
        settings.setdefault('connection_timeout', 5)
        self.connection = mysql.connector.connect(**settings)
        # Tables come from setup.sql.
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT id FROM users WHERE id = %s', (0,))
            cursor.fetchall()
            cursor.execute('SELECT user_id FROM workspaces WHERE user_id = %s', (0,))
            cursor.fetchall()
            self.connection.commit()
            cursor.close()
        except mysql.connector.Error:
            self.connection.close()
            raise

    def open_cursor(self):
        # Reconnect if needed.
        self.connection.ping(reconnect=True, attempts=1, delay=0)
        return self.connection.cursor(buffered=True)

    def sign_up(self, username, password):
        username = username.strip().lower()
        if not re.fullmatch(r'[a-z0-9_.-]{3,32}', username):
            raise ValueError('Use 3–32 letters, numbers, dots, underscores or hyphens for your username.')
        if not 8 <= len(password) <= 128 or not password.strip():
            raise ValueError('Use a password of 8–128 characters, not just spaces.')
        salt = secrets.token_bytes(16)
        password_hash = self.hash_password(password, salt)
        cursor = self.open_cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, salt, password_hash) VALUES (%s, %s, %s)',
                (username, salt.hex(), password_hash))
            user_id = cursor.lastrowid
            self.connection.commit()
            return user_id
        except mysql.connector.Error as exc:
            self.connection.rollback()
            if exc.errno == 1062:
                raise ValueError('That username is already taken.') from exc
            raise
        finally:
            cursor.close()

    @staticmethod
    def hash_password(password, salt):
        # Hash passwords in Python.
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, PASSWORD_ROUNDS).hex()

    def log_in(self, username, password):
        if len(password) > 128:
            raise ValueError('Incorrect username or password.')
        cursor = self.open_cursor()
        try:
            cursor.execute(
                'SELECT id, salt, password_hash FROM users WHERE username = %s',
                (username.strip().lower(),))
            row = cursor.fetchone()
            self.connection.commit()
        finally:
            cursor.close()
        salt = bytes.fromhex(row[1]) if row else bytes(16)
        candidate = self.hash_password(password, salt)
        if not row or not hmac.compare_digest(row[2], candidate):
            raise ValueError('Incorrect username or password.')
        return row[0]

    def save(self, user_id, data):
        # Store inputs as JSON text.
        text = json.dumps(data, ensure_ascii=False)
        saved_at = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        cursor = self.open_cursor()
        try:
            cursor.execute('SELECT user_id FROM workspaces WHERE user_id = %s', (user_id,))
            if cursor.fetchone() is None:
                cursor.execute(
                    'INSERT INTO workspaces (user_id, data, saved_at) VALUES (%s, %s, %s)',
                    (user_id, text, saved_at))
            else:
                cursor.execute(
                    'UPDATE workspaces SET data = %s, saved_at = %s WHERE user_id = %s',
                    (text, saved_at, user_id))
            self.connection.commit()
        except mysql.connector.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def load(self, user_id):
        cursor = self.open_cursor()
        try:
            cursor.execute('SELECT data, saved_at FROM workspaces WHERE user_id = %s', (user_id,))
            row = cursor.fetchone()
            self.connection.commit()
        finally:
            cursor.close()
        if row is None:
            return {}, None
        try:
            data = json.loads(row[0])
            if not isinstance(data, dict):
                raise ValueError
        except (ValueError, TypeError) as exc:
            raise ValueError('Saved data could not be read. Keep a database backup before repairing it.') from exc
        return data, row[1]

    def close(self):
        self.connection.close()
