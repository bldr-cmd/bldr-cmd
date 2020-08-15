import click

VERSION = "0.0.1"

@click.group()
def main():
    click.echo(f"bldr - {VERSION}")


@main.command('gen.up')
def gen_up():
    click.echo('Syncing')
