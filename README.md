# Toronto Lobbyist Registry Tools

A tool for processing Toronto's lobbyist data.

The [City of Toronto Lobbyist Registrar][registrar] conveniently make available
[its open data][data] from the registry on the City's open data portal in XML
format.

This code repository consists of:

1. A command-line tool for converting the raw XML into CSV.
1. A command-line tool for uploading this CSV to a Google Spreadsheet.
1. A configuration to run the tool nightly in the cloud.

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
