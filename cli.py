import click
from commands.parse_xml import parse_xml
from commands.update_graphcommons import update_graphcommons

CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

cli.add_command(parse_xml)
cli.add_command(update_graphcommons)

if __name__ == '__main__':
    cli()

