# Toronto Lobbyist Registry Tools

A tool for processing Toronto's lobbyist data.

The [City of Toronto Lobbyist Registrar][registrar] conveniently make available
[its open data][data] from the registry on the City's open data portal in XML
format.

This code repository consists of:

1. A command-line tool for:
  - converting the raw XML into CSV.
  - uploading this CSV to a Google Spreadsheet. [:memo: CSV][csv]
  - updating an online visualization of the relationships
    [:globe_with_meridians: Graph][graph]
1. A configuration to run the tool nightly in the cloud.
   [:scroll: Logs][ci-master]

## Usage

To prepare your local development environment for the first time:

```
# Install Python package dependencies
$ pipenv install

# If you would like to set some configuration from environment variables,
# use this scaffold file.
cp sample.env .env
```

### Command: `parse-xml`

To process the xml file into spreadsheet format on either the local
filesystem or Google Spreadsheet.

```
$ pipenv run python cli.py parse-xml --help

Usage: cli.py parse-xml [OPTIONS] XML_FILE

  Process XML file of Toronto lobbyist registry data into a CSV file.

  TODO: Document how to generate Google service account credentials.

Options:
  -o, --output-file <file.csv>  If provided, will write local CSV file.
                                Default: print to screen
  --output-gsheet <url/key>     If provided with writable Google spreadsheet
                                URL, CSV will be uploaded.
  --google-creds <file>         JSON keyfile with Google service account
                                credentials. Default: service-key.json
  -h, --help                    Show this message and exit.
```

![Screenshot of running the command](/docs/screenshot.png)

### Command: `update-graphcommons`

For updating a GraphCommons visualization from the XML.

```
$ pipenv run python cli.py update-graphcommons --help
Usage: cli.py update-graphcommons [OPTIONS] XML_FILE

Options:
  --graph-id <string>  Graph Commons graph ID (find in graph url)
  --api-key <string>   Graph Commons API key  [required]
  -h, --help           Show this message and exit.
```

## Technologies Used

- **Python.** A programming language common in scripting.
- [**Click.**][click] A Python library for writing simple command-line
  tools.
- [**CircleCI.**][circleci] A script-running service that [runs scheduled
  tasks][circleci-cron] for us in the cloud.

<!-- Links -->
   [data]: https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#94202791-cb02-4a98-4b1f-0f301b6f89d3
   [registrar]: https://www.toronto.ca/city-government/accountability-operations-customer-service/accountability-officers/lobbyist-registrar/
   [click]: http://click.pocoo.org/7/
   [circleci]: https://circleci.com/docs/2.0/about-circleci/
   [circleci-cron]: https://support.circleci.com/hc/en-us/articles/115015481128-Scheduling-jobs-cron-for-builds-
   [ci-workflow]: https://circleci.com/gh/patcon/workflows/toronto-lobbyist-registry-tools
   [ci-master]: https://circleci.com/gh/patcon/toronto-lobbyist-registry-tools/tree/master
   [csv]: https://docs.google.com/spreadsheets/d/1uCaEMd5jHKSaFwoLXhj06uB0AEca-hpK0Tr3E2jFTk8/edit#gid=472973700
