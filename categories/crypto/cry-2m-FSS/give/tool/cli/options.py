import click
from cli.constants import *


def with_minimum_option(func):
    return click.option(
        '-m', '--minimum',
        type=int,
        metavar='M',
        default=5,
        help='Minimum num of shares to recover secret',
    )(func)

def with_number_option(func):
    return click.option(
        '-n', '--number',
        type=int,
        metavar='N',
        default=6,
        help='Number of shares',
    )(func)

def with_file_option(func):
    return click.option(
        '-f', '--file',
        type=click.Path(exists=True),
        metavar='FILE',
        default=DEFAULT_FILE,
        help='File to encrypt path',
    )(func)

def with_dir_option(func):
    return click.option(
        '-d', '--dir',
        type=click.Path(exists=True),
        metavar='DIR',
        default=SHARES_DIR,
        help='Directory to encrypt path',
    )(func)

def with_params_option(func):
    return click.option(
        '-p', '--params',
        type=click.Path(exists=True),
        metavar='PARAMS',
        default= None,
        help='Parametrs for FSS',
    )(func)

def with_key_option(func):
    return click.option(
        '-k', '--key',
        type=click.Path(exists=True),
        metavar='KEY',
        default=None,
        help='Key for AES in FSS',
    )(func)

def with_iv_option(func):
    return click.option(
        '-i', '--iv',
        type=click.Path(exists=True),
        metavar='IV',
        default=None,
        help='IV for AES in FSS',
    )(func)