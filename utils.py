import csv
import urllib.parse

from io import StringIO


def generate_csv(rows):
    csvfile = StringIO()
    writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    return csvfile.getvalue()

def get_if_exists(tree, xpath):
    result = tree.xpath(xpath)
    if result:
        return result[0].text

    return ''

def alturlsplit(url):
    url_data = urllib.parse.urlsplit(url)
    query_data = urllib.parse.parse_qs(url_data.query)
    url_data = url_data._replace(query=query_data)
    return url_data

def alturlunsplit(url_data):
    query_data = url_data.query
    query_string = '&'.join(['{}={}'.format(k, v) for k, v in query_data.items()])
    url_data = url_data._replace(query=query_string)
    url = urllib.parse.urlunsplit(url_data)
    return url
