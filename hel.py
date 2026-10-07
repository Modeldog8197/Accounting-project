"""Compatibility entry point for the redesigned health page."""

from app import launch


def load_hel_page():
    launch('health')


if __name__ == '__main__':
    launch('health')
