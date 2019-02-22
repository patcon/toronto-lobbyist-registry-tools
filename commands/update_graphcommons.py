import click
import os

from graphcommons import GraphCommons, Signal
from lxml import etree


CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('xml-file')
@click.option('--graph-id',
              default='a19db181-31d2-4b57-b37e-312365173da7',
              metavar='<string>',
              )
@click.option('--api-key',
              required=True,
              help='Graph Commons API key',
              envvar='GRAPH_COMMONS_API_KEY',
              metavar='<string>',
              )
def update_graphcommons(xml_file, graph_id, api_key):

    client = GraphCommons(api_key)

    graph = client.graphs(graph_id)
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    tree = etree.parse(xml_file).getroot()
    rows = tree.xpath('/ROWSET/ROW')
    signals = []
    registrations = []

    for i, r in enumerate(rows):
        i = i + 1
        if i % 10 == 0:
                click.echo('Processing row {}/{}\r'.format(i, len(rows)), err=True, nl=False)
        if i == len(rows):
                click.echo('Processing row {}/{}'.format(i, len(rows)), err=True, nl=True)
        reg = {
            'SMNumber': r.xpath('./SMNumber/text()').pop(),
        }
        registrations.append(reg)

    for r in registrations:
        node_existing = [n for n in nodes if n['name'] == r['SMNumber']]
        if node_existing:
            enode = node_existing.pop()
            # update signal
            sig = Signal(
                id=enode['id'],
                action='node_update',
                name=r['SMNumber'],
                type='Subject Matter',
            )
        else:
            # create signal
            sig = Signal(
                action='node_create',
                name=r['SMNumber'],
                type='Subject Matter',
            )
        signals.append(sig)

    #click.echo('Clearing graph...')
    #client.clear_graph(graph_id)
    click.echo('Updating graph...')
    client.update_graph(
        id=graph_id,
        signals=signals[0:999],
    )
