import csv
import gspread
from io import StringIO
from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials


DEBUG = False

tree = etree.parse('data/lobbyactivity-active.xml').getroot()
rows = tree.xpath('/ROWSET/ROW')
entries = []

def get_if_exists(tree, xpath):
    result = tree.xpath(xpath)
    if result:
        return result[0].text

    return ''

for r in rows:
    entry = {}
    entry['subject_matter_id'] = r.xpath('./SMNumber')[0].text
    entry['registrant_id']     = r.xpath('./Registrant/RegistrationNUmber')[0].text
    for c in r.xpath('./Communications/Communication'):
        entry['lobbied_person'] = get_if_exists(c, './POH_Name')
        entry['lobbied_office'] = get_if_exists(c, './POH_Office')
        entries.append(entry)

csvfile = StringIO()
fields = ['subject_matter_id', 'registrant_id', 'lobbied_person', 'lobbied_office']
writer = csv.DictWriter(csvfile, fieldnames=fields)
writer.writeheader()
for e in entries:
    writer.writerow(e)

if DEBUG:
    with open('data/registry.csv', 'w') as f:
        f.write(csvfile.getvalue())
else:
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('service-key.json', scope)
    gc = gspread.authorize(credentials)
    spreadsheet_id = '1uCaEMd5jHKSaFwoLXhj06uB0AEca-hpK0Tr3E2jFTk8'
    gc.import_csv(spreadsheet_id, csvfile.getvalue())
