import click
from commands.parse_xml import parse_xml

CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

cli.add_command(parse_xml)

if __name__ == '__main__':
    cli()

