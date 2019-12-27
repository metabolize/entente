#!/usr/bin/env python3

import os
import click
from executor import execute


def python_source_files():
    import glob

    return glob.glob("*.py") + ["entente/", "doc/"]


@click.group()
def cli():
    pass


@cli.command()
def init():
    execute("pip install --upgrade -r requirements_dev.txt")


@cli.command()
def clean():
    execute("find . -name '*.pyc' -or -name '__pycache__' -delete")


def docker_repo(python_version, tag):
    return "laceproject/entente-ci-{}:{}".format(python_version, tag)


@cli.command()
@click.argument("tag")
def docker_build(tag):
    execute(
        "docker",
        "build",
        "-t",
        docker_repo("3.6", tag),
        "-f",
        "docker/Dockerfile",
        ".",
    )


@cli.command()
@click.argument("tag")
def docker_push(tag):
    """
    When pushing a new version, bump the minor version. It's okay to re-push,
    though once it's being used in master, you should leave it alone.
    """
    execute("docker", "push", docker_repo("3.6", tag))


@cli.command()
def test():
    execute("pytest")


@cli.command()
def coverage():
    execute("pytest --cov=entente")


@cli.command()
def coverage_report():
    execute("coverage html")
    execute("open htmlcov/index.html")


@cli.command()
def lint():
    execute("flake8", *python_source_files())


@cli.command()
def black():
    execute("black", *python_source_files())


@cli.command()
def black_check():
    execute("black", "--check", *python_source_files())


@cli.command()
def doc():
    execute("rm -rf build/ doc/build/ doc/api/")
    execute("sphinx-build -W -b html doc doc/build")


@cli.command()
def doc_open():
    execute("open doc/build/index.html")


@cli.command()
def publish():
    execute("rm -rf dist/")
    execute("python3 setup.py sdist bdist_wheel")
    execute("twine upload dist/*")


if __name__ == "__main__":
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    cli()
