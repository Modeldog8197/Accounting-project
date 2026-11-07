"""Use a separate MySQL database so tests cannot clear real application data."""

import unittest
from pathlib import Path

import mysql.connector


def prepare_database():
    try:
        from db_config_test import DB_CONFIG
    except ImportError:
        raise unittest.SkipTest('Create db_config_test.py for MySQL integration tests; see README.md.')
    config = dict(DB_CONFIG)
    if config.get('database') != 'wellledger_test':
        raise ValueError('Tests may only use the database named wellledger_test.')
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    try:
        # Skip CREATE DATABASE and USE: the test connection already selects its database.
        statements = Path(__file__).with_name('setup.sql').read_text().split(';')[2:]
        for statement in statements:
            if statement.strip(): cursor.execute(statement)
        cursor.execute('DELETE FROM workspaces')
        cursor.execute('DELETE FROM users')
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    return config
