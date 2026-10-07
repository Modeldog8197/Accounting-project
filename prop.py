"""Compatibility entry point for the redesigned home page."""

from app import launch


def load_prop_page(userdata):
    launch('home', userdata)


if __name__ == '__main__':
    launch('home')
