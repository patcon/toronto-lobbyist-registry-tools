import click
import os

from graphcommons import GraphCommons, Signal
from lxml import objectify


CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('xml-file')
@click.option('--graph-id',
              required=True,
              help='Graph Commons graph ID (find in graph url)',
              envvar='GRAPH_COMMONS_GRAPH_ID',
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

    signals = []
    registrations = []
    topics_relations = []

    signals.append(Signal(
        action='nodetype_create',
        name='Topic',
    ))
    signals.append(Signal(
        action='nodetype_create',
        name='Registration',
    ))
    signals.append(Signal(
        action='edgetype_create',
        name='RELATES TO',
    ))

    tree = objectify.parse(xml_file).getroot()
    rows = tree.ROW

    for i, r in enumerate(rows):
        i = i + 1
        if i % 10 == 0:
                click.echo('Processing row {}/{}\r'.format(i, len(rows)), err=True, nl=False)
        if i == len(rows):
                click.echo('Processing row {}/{}'.format(i, len(rows)), err=True, nl=True)
        communications = []
        if hasattr(r, 'Communications'):
            for c in r.Communications.Communication:
                discard_keys = ['LobbyistBusinessAddress']
                # Converting to dict with strings.
                comm = {str(k): str(c.__dict__[k]) for k in c.__dict__.keys() if (k not in discard_keys)}
                comm['CommunicationMethod'] = comm['CommunicationMethod'].split(';')
                for m in comm['CommunicationMethod']:
                    COMM_METHODS = ['Meeting', 'Telephone', 'E-mail', '', 'MeetingsArranged', 'Written']
                    if m not in COMM_METHODS and not m.startswith('Other:'):
                        raise 'Unexpected CommunicationMethod found...'
                comm['InvolvedMeeting'] = True if 'Meeting' in comm['CommunicationMethod'] else False
                comm['InvolvedTelephone'] = True if 'Telephone' in comm['CommunicationMethod'] else False
                comm['InvolvedEmail'] = True if 'E-mail' in comm['CommunicationMethod'] else False
                comm['InvolvedOther'] = True if any([m.startswith("Other:") for m in comm['CommunicationMethod']]) else False
                # TODO: Gather OtherDescription.
                communications.append(comm)

        discard_keys = ['Firms', 'Beneficiaries', 'Registrant', 'Communications']
        # Converting to dict with strings.
        reg = {str(k): str(r.__dict__[k]) for k in r.__dict__.keys() if (k not in discard_keys)}
        reg['SubjectMatter'] = reg['SubjectMatter'].split(';')
        registrations.append(reg)

    topics = []
    click.echo('Generating signals to modify graph...')
    for r in registrations:
        node_existing = [n for n in nodes if n['name'] == r['SMNumber']]
        for sm in r['SubjectMatter']:
            if sm not in topics:
                topics.append(sm)
                topic = [n for n in nodes if n['name'] == sm]
                if topic:
                    topic = topic.pop()
                    sig = Signal(
                        action='node_update',
                        id=topic['id'],
                        name=sm,
                        type='Topic',
                    )
                else:
                    sig = Signal(
                        action='node_create',
                        name=sm,
                        type='Topic',
                    )
                signals.append(sig)
            edge = [e for e in edges if graph.get_node(e['from'])['name'] == r['SMNumber'] and graph.get_node(e['to'])['name'] == sm]
            if edge:
                # Update
                edge = edge.pop()
                #sig = Signal(
                #    action='edge_update',
                #    id=edge['id'],
                #)
                pass
            else:
                # Create
                sig = Signal(
                    action='edge_create',
                    name='RELATES TO',
                    from_type='Registration',
                    from_name=r['SMNumber'],
                    to_type='Topic',
                    to_name=sm,
                )
                signals.append(sig)

        if node_existing:
            enode = node_existing.pop()
            # update signal
            sig = Signal(
                id=enode['id'],
                action='node_update',
                name=r['SMNumber'],
                type='Registration',
                properties={
                    'particulars': r['Particulars'],
                },
            )
        else:
            # create signal
            sig = Signal(
                action='node_create',
                name=r['SMNumber'],
                type='Registration',
                properties={
                    'particulars': r['Particulars'],
                },
            )
        signals.append(sig)

    #click.echo('Clearing graph...')
    #client.clear_graph(graph_id)

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    for chunk in chunks(signals, 1000):
        click.echo('Updating chunk...')
        client.update_graph(
            id=graph_id,
            signals=chunk,
        )
