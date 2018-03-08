import pymode

m = pymode.Mode('<your-org-name>','<your-api-token>','<your-api-password>')

# Grab list of all visible Data Sources
data_sources = m.get_data_sources()

# Iterate through list of Data Sources and print relevant information
for ds in data_sources:
    print('Data Source Name: {}, Data Source ID: {}'.format(ds.name, ds.id))

def mass_update_data_source(old_data_source_id, new_data_source_id):
    """Updates the Data Source for a group of Queries currently using the same Data Source."""

    spaces = m.get_spaces()

    for space in spaces:
        reports = space.get_reports()
        for report in reports:
            queries = report.get_queries()
            for query in queries:
                if query.data_source_id == old_data_source_id:
                    resp = query.update_data_source(new_data_source_id)

    return resp

mass_update_data_source(<insert-old-data-source-id>, <insert-new-data-source-id>)
