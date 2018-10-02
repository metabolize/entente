#!/usr/bin/env python

import click
import glob
from executor import execute

def nose_cmd():
    # More reliably locate this command when more than one Python are
    # installed.
    try:
        execute("nose2-2.7 --help", capture=True)
        return "nose2-2.7"
    except:
        return "nose2"


@click.group()
def cli():
    pass


@cli.command()
def init():
    execute("pip install -r requirements_dev.txt")


@cli.command()
def test():
    execute(nose_cmd())


source_files = glob.glob("*.py") + ["entente/", "doc/"]


@cli.command()
def lint():
    execute("pyflakes", *source_files)


@cli.command()
def black():
    execute("black", *source_files)


@cli.command()
def black_check():
    execute("black", "--check", *source_files)


@cli.command()
def doc():
    execute("rm -rf build/ doc/build/ doc/api/")
    execute("sphinx-build -b html doc doc/build")


@cli.command()
def doc_open():
    execute("open doc/build/index.html")


@cli.command()
def upload():
    execute("rm -rf dist/")
    execute("python setup.py sdist")
    execute("twine upload dist/*")


if __name__ == "__main__":
    cli()
