import click
import csv
import gspread
import os
import urllib.parse

from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials

from utils import generate_csv, get_if_exists


CONTEXT_SETTINGS = dict(help_option_names=['--help', '-h'])
GOOGLE_SCOPES = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('xml-file')
@click.option('--output-file', '-o',
              required=False,
              help='If provided, will write local CSV file. Default: print to screen',
              metavar='<file.csv>',
              )
@click.option('--output-gsheet',
              required=False,
              help='If provided with writable Google spreadsheet URL, CSV will be uploaded.',
              metavar='<url/key>'
              )
@click.option('--google-creds',
              default='service-key.json',
              required=False,
              help='JSON keyfile with Google service account credentials. Default: service-key.json',
              metavar='<file>',
              )
def parse_xml(xml_file, output_file, output_gsheet, google_creds):
    """Process XML file of Toronto lobbyist registry data into a CSV file.

    TODO: Document how to generate Google service account credentials.
    """
    tree = etree.parse(xml_file).getroot()
    rows = tree.xpath('/ROWSET/ROW')
    communications = []

    for i, r in enumerate(rows):
        i = i + 1
        if i % 10 == 0:
                click.echo('Processing row {}/{}\r'.format(i, len(rows)), err=True, nl=False)
        if i == len(rows):
                click.echo('Processing row {}/{}'.format(i, len(rows)), err=True, nl=True)
        subject_matter = {}
        sm_fields = [
            'SMNumber',
            'SubjectMatter',
            'Particulars',
        ]
        for f in sm_fields:
            subject_matter[f] = get_if_exists(r, './'+f)

        ## Business / Organization
        # We are only using the first Firm for now.
        # TODO: Be smarter with this. Maybe select the most important one via some criteria.
        firm_name = r.xpath('./Firms/Firm[1]/Name/text()').pop()

        ## Communications
        for c in r.xpath('./Communications/Communication'):
            comm = {}
            comm.update(subject_matter)
            comm['FirmName'] = firm_name
            fields = [
                'LobbyistNumber',
                'LobbyistPositionTitle',
                'LobbyistFirstName',
                'LobbyistLastName',
                'POH_Office',
                'POH_Type',
                'POH_Position',
                'POH_Name',
                'CommunicationDate',
            ]
            for f in fields:
                comm[f] = get_if_exists(c, './'+f)
            communications.append(comm)

    content = generate_csv(communications)

    if output_file:
        click.echo('Writing CSV data to: ' + output_file, err=True)
        with open(output_file, 'w') as f:
            f.write(content)
    elif not output_gsheet:
        click.echo(content)

    if output_gsheet and google_creds:
        url_data = urllib.parse.urlsplit(output_gsheet)
        if url_data.netloc == 'docs.google.com':
            spreadsheet_key = url_data.path.split('/')[3]
        else:
            spreadsheet_key = output_gsheet

        click.echo('Writing CSV data to: https://docs.google.com/spreadsheets/d/{}'.format(spreadsheet_key), err=True)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(google_creds, GOOGLE_SCOPES)
        gc = gspread.authorize(credentials)
        gc.import_csv(spreadsheet_key, content)

if __name__ == '__main__':
    parse_xml()
