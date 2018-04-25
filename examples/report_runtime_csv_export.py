import pymode
import csv

ORG = 'your-org-name-here'
API_TOKEN = 'your-api-token-here'
API_PASSWORD = 'your-api-password-here'

m = pymode.Mode(ORG, API_TOKEN, API_PASSWORD)

# Empty array for report attributes that we want
reports_attributes = []

base_url = 'https://modeanalytics.com/{}/reports/'.format(ORG)

# Iterate through spaces and get reports for them
spaces = m.get_spaces()

for space in spaces:
	reports = space.get_reports()

# For each report grab relevant information and put it into the reports_attributes
	for report in reports:
		report_url = base_url + report.token
		report_name = report.name
		report_runtime = report.expected_runtime
		last_run = report.last_run_at
		reports_attributes.append( {'name' : report_name, 'runtime': report_runtime, 'url': report_url, 'last_run': last_run})

keys = reports_attributes[0].keys()

# Write ou the CSV
with open('reports.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(reports_attributes)
