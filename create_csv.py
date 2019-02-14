import csv
import gspread
from io import StringIO
from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials


DEBUG = False

tree = etree.parse('data/lobbyactivity-active.xml').getroot()
rows = tree.xpath('/ROWSET/ROW')
communications = []

def get_if_exists(tree, xpath):
    result = tree.xpath(xpath)
    if result:
        return result[0].text

    return ''

for r in rows:
    subject_matter_number = r.xpath('./SMNumber')[0].text
    for c in r.xpath('./Communications/Communication'):
        fields = [
            'LobbyistNumber',
            'LobbyistPositionTitle',
            'LobbyistFirstName',
            'LobbyistMiddleInitial',
            'LobbyistLastName',
            'SMNumber',
            'POH_Office',
            'POH_Type',
            'POH_Position',
            'POH_Name',
            'CommunicationDate',
        ]
        comm = {}
        comm['SMNumber'] = subject_matter_number
        for f in fields:
            comm[f] = get_if_exists(c, './'+f)
        print(comm['CommunicationDate'])
        communications.append(comm)

csvfile = StringIO()
writer = csv.DictWriter(csvfile, fieldnames=fields)
writer.writeheader()
for c in communications:
    writer.writerow(c)

if DEBUG:
    with open('data/communications.csv', 'w') as f:
        f.write(csvfile.getvalue())
else:
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('service-key.json', scope)
    gc = gspread.authorize(credentials)
    spreadsheet_id = '1uCaEMd5jHKSaFwoLXhj06uB0AEca-hpK0Tr3E2jFTk8'
    gc.import_csv(spreadsheet_id, csvfile.getvalue())
