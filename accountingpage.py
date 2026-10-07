"""Compatibility entry point for the redesigned accounting page."""

from app import launch


def load_acc_page():
    launch('accounting')


if __name__ == '__main__':
    launch('accounting')
