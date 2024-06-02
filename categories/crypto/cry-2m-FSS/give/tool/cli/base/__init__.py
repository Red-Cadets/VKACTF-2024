import click

from .bind import bind
from .split import split



def register(cli: click.Group):
    cli.add_command(bind)
    cli.add_command(split)

__all__ = ("register",)