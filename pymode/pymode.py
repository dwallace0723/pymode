import os
import requests
import json

API_TOKEN = os.environ.get('MODE_API_TOKEN')
API_PASSWORD = os.environ.get('MODE_API_PASSWORD')

class Requester(object):

	def __init__(self, account_name, api_token, api_password):
		self.api_base = 'https://modeanalytics.com/api/{}'.format(account_name)
		self.api_token = api_token
		self.api_password = api_password
		self.account_name = account_name

	def _get(self, url_suffix):
		url = self.api_base + url_suffix
		response = requests.get(url, auth=(self.api_token, self.api_password))
		if response.status_code == requests.codes.ok:
			return response.json()
		else:
			raise RuntimeError(response.status_code)

	def _post(self, url_suffix):
		url = self.api_base + url_suffix
		response = requests.post(url, auth=(self.api_token, self.api_password))
		return response

	def _patch(self, url_suffix, payload=None):
		url = self.api_base + url_suffix
		headers = {'Content-Type': 'application/json'}
		response = requests.patch(url=url, json=payload, headers=headers, auth=(self.api_token, self.api_password))
		return response

	def _delete(self, url_suffix):
		url = self.api_base + url_suffix
		response = requests.delete(url, auth=(self.api_token, self.api_password))
		return response

class Mode(object):

	def __init__(self, account_name, api_token=API_TOKEN, api_password=API_PASSWORD):
		self.account_name = account_name
		self.api_token = api_token
		self.api_password = api_password

		self.requester = Requester(self.account_name, self.api_token, self.api_password)

	def get_memberships(self):
		resp = self.requester._get('/memberships')
		memberships = resp.get('_embedded').get('memberships')
		memberships = [Membership(membership, self.requester) for membership in memberships]

		return memberships

	def get_membership(self, membership_token):
		resp = self.requester._get('/memberships/{}'.format(membership_token))
		return Membership(resp, self.requester)

	def get_data_source(self, data_source_token):
		resp = self.requester._get('/data_sources/{}'.format(data_source_token))
		return DataSource(resp, self.requester)

	def get_data_sources(self):
		resp = self.requester._get('/data_sources')
		data_sources = resp.get('_embedded').get('data_sources')
		data_sources = [DataSource(data_source, self.requester) for data_source in data_sources]

		return data_sources

	def get_definitions(self):
		resp = self.requester._get('/definitions')
		definitions = resp.get('_embedded').get('definitions')
		definitions = [Definition(definition, self.requester) for definition in definitions]

		return definitions

	def get_report(self, report_token):
		resp = self.requester._get('/reports/{}'.format(report_token))
		return Report(resp, self.requester)

	def get_report_run(self, report_token, report_run_token):
		resp = self.requester._get('/reports/{}/runs/{}'.format(report_token, report_run_token))
		return ReportRun(resp, report_token, self.requester)

	def get_query(self, report_token, query_token):
		resp = self.requester._get('/reports/{}/queries/{}'.format(report_token, query_token))
		return Query(resp, report_token, self.requester)

	def get_space(self, space_token):
		resp = self.requester._get('/spaces/{}'.format(space_token))
		return Space(resp, self.requester)

	def get_spaces(self):
		resp = self.requester._get('/spaces')
		spaces = resp.get('_embedded').get('spaces')
		spaces_list = [Space(space, self.requester) for space in spaces]

		if resp.get('pagination'):
			while resp.get('pagination').get('page') < resp.get('pagination').get('total_pages'):
				next_page = resp.get('pagination').get('page')+1
				resp = self.requester._get('/spaces?page={}'.format(self.token, next_page))
				spaces = resp.get('_embedded').get('spaces')
				for space in spaces:
					space_instance = Space(space, self.token, self.requester)
					spaces_list.append(space_instance)

		return spaces_list

class Definition(object):

	def __init__(self, data, requester):
		self.token = data.get('token')
		self.id = data.get('id')
		self.name = data.get('name')
		self.description = data.get('description')
		self.source = data.get('source')
		self.data_source_id = data.get('data_source_id')
		self.created_at = data.get('created_at')
		self.updated_at = data.get('updated_at')
		self.last_successful_github_sync_id = data.get('last_successful_github_sync_id')
		self.last_successful_sync_at = data.get('last_successful_sync_at')

		self.requester = requester

class DataSource(object):

	def __init__(self, data, requester):
		self.token = data.get('token')
		self.id = data.get('id')
		self.name = data.get('name')
		self.description = data.get('description')
		self.adapter = data.get('adapter')
		self.created_at = data.get('created_at')
		self.updated_at = data.get('updated_at')
		self.has_expensive_schema_updates = data.get('has_expensive_schema_updates')
		self.public = data.get('public')
		self.asleep = data.get('asleep')
		self.queryable = data.get('queryable')
		self.display_name = data.get('display_name')
		self.account_id = data.get('account_id')
		self.account_username = data.get('account_username')
		self.organization_token = data.get('organization_token')
		self.default = data.get('default')
		self.default_for_organization_id = data.get('default_for_organization_id')
		self.database = data.get('database')
		self.host = data.get('host')
		self.port = data.get('port')
		self.ssl = data.get('ssl')
		self.username = data.get('username')
		self.provider = data.get('provider')
		self.vendor = data.get('vendor')
		self.ldap = data.get('ldap')
		self.warehouse = data.get('warehouse')
		self.bridged = data.get('bridged')
		self.custom_attributes = data.get('custom_attributes')

		self.requester = requester


class Space(object):

	def __init__(self, data, requester):
		self.token = data.get('token')
		self.id = data.get('id')
		self.space_type = data.get('space_type')
		self.name = data.get('name')
		self.description = data.get('description')
		self.state = data.get('state')
		self.restricted = data.get('restricted')

		self.requester = requester

	def get_reports(self):
		resp = self.requester._get('/spaces/{}/reports'.format(self.token))
		reports = resp.get('_embedded').get('reports')
		report_list = [Report(report, self.requester) for report in reports]

		if resp.get('pagination'):
			while resp.get('pagination').get('page') < resp.get('pagination').get('total_pages'):
				next_page = resp.get('pagination').get('page')+1
				resp = self.requester._get('/spaces/{}/reports?page={}'.format(self.token, next_page))
				reports = resp.get('_embedded').get('reports')
				for report in reports:
					report_instance = Report(report, self.token, self.requester)
					report_list.append(report_instance)

		return report_list

class Membership(object):

	def __init__(self, data, requester):
		self.token = data.get('_links').get('self').get('href').split('memberships/')[1]
		self.user = data.get('_links').get('user').get('href').split('api/')[1]
		self.admin = data.get('admin')

		self.requester = requester

class User(object):

	def __init__(self, data, requester):
		self.token = data.get('token')
		self.id = data.get('id')
		self.username = data.get('username')
		self.name = data.get('name')
		self.email = data.get('email')
		self.email_verified = data.get('email_verified')
		self.user = data.get('user')

		self.requester = requester

class Report(object):

	def __init__(self, data, requester):
		self.token = data.get('token')
		self.id = data.get('id')
		self.name = data.get('name')
		self.description = data.get('description')
		self.created_at = data.get('created_at')
		self.updated_at = data.get('updated_at')
		self.edited_at = data.get('edited_at')
		self.theme_id = data.get('theme_id')
		self.archived = data.get('archived')
		self.space_token = data.get('space_token')
		self.account_id = data.get('account_id')
		self.account_username = data.get('account_username')
		self.public = data.get('public')
		self.full_width = data.get('full_width')
		self.manual_run_disabled = data.get('manual_run_disabled')
		self.run_privately = data.get('run_privately')
		self.layout = data.get('layout')
		self.is_embedded = data.get('is_embedded')
		self.is_signed = data.get('is_signed')
		self.shared = data.get('shared')
		self.expected_runtime = data.get('expected_runtime')
		self.last_successfully_run_at = data.get('last_successfully_run_at')
		self.last_run_at = data.get('last_run_at')
		self.web_preview_image = data.get('web_preview_image')
		self.last_successful_run_token = data.get('last_successful_run_token')
		self.published = data.get('_forms').get('edit').get('input').get('report').get('published').get('value')

		self.requester = requester

	def run(self):
		resp = self.requester._post('/reports/{}/runs'.format(self.token))
		if resp.status_code == 202:
			print('Report {} ({}) run queued'.format(self.token, self.name))
		else:
			print('Report Run Failed')

		return resp

	def archive(self):
		if self.archived:
			resp = 'Skipped: Report {} ({}) already archived'.format(self.token, self.name)
		else:
			resp = self.requester._patch('/reports/{}/archive'.format(self.token))
			if resp.status_code == requests.codes.ok:
				print('Report {} ({}) archived'.format(self.token, self.name))
				self.archived = True
			else:
				print('Report {} ({}) failed to archive'.format(self.token, self.name))

		return resp

	def unarchive(self):
		if not self.archived:
			resp = 'Skipped: Report {} ({}) not archived'.format(self.token, self.name)
		else:
			resp = self.requester._patch('/reports/{}/unarchive'.format(self.token))
			if resp.status_code == requests.codes.ok:
				print('Report {} ({}) unarchived'.format(self.token, self.name))
				self.archived = False
			else:
				print('Report {} ({}) failed to unarchive'.format(self.token, self.name))

		return resp

	def delete(self):
		resp = self.requester._delete('/reports/{}'.format(self.token))
		if resp.status_code == requests.codes.ok:
			print('Report {} ({}) deleted'.format(self.token, self.name))
		else:
			print('Report {} ({}) failed to delete'.format(self.token, self.name))

		return resp

	def get_runs(self):
		resp = self.requester._get('/reports/{}/runs'.format(self.token))
		report_runs = resp.get('_embedded').get('report_runs')
		report_run_list = [ReportRun(report_run, self.token, self.requester) for report_run in report_runs]

		if resp.get('pagination'):
			while resp.get('pagination').get('page') < resp.get('pagination').get('total_pages'):
				next_page = resp.get('pagination').get('page')+1
				resp = self.requester._get('/reports/{}/runs?page={}'.format(self.token, next_page))
				report_runs = resp.get('_embedded').get('report_runs')
				for report_run in report_runs:
					report_run_instance = ReportRun(report_run, self.token, self.requester)
					report_run_list.append(report_run_instance)

		return report_run_list

	def get_queries(self):
		resp = self.requester._get('/reports/{}/queries'.format(self.token))
		queries = resp.get('_embedded').get('queries')
		query_list = [Query(query, self.token, self.requester) for query in queries]

		if resp.get('pagination'):
			while resp.get('pagination').get('page') < resp.get('pagination').get('total_pages'):
				next_page = resp.get('pagination').get('page')+1
				resp = self.requester._get('/reports/{}/queries?page={}'.format(self.token, next_page))
				queries = resp.get('_embedded').get('queries')
				for query in queries:
					query_instance = Query(query, self.token, self.requester)
					query_list.append(query_instance)

		return query_list

	def update_description(self, description):
		if self.description == description:
			print('Report {} ({}) skipped'.format(self.token, self.name))
		else:
			payload = {'report':{
				'name': self.name,
				'layout': self.layout,
				'description': description,
				'account_id': self.account_id,
				'space_token': self.space_token,
				'published': self.published
				}
			}

			resp = self.requester._patch('/reports/{}'.format(self.token), payload=payload)
			if resp.status_code == 202:
				print('Report {} ({}) description updated'.format(self.token, self.name, description))
				self.description = description
			else:
				print('Report {} ({}) failed to update description'.format(self.token, self.name, description))

		return resp

	def update_space(self, space_token):
		if self.space_token == space_token:
			print('Report {} ({}) already in Space {}'.format(self.token, self.name, space_token))
		else:
			payload = {'report':{
				'name': self.name,
				'layout': self.layout,
				'description': self.description,
				'account_id': self.account_id,
				'space_token': space_token,
				'published': self.published
				}
			}

			resp = self.requester._patch('/reports/{}'.format(self.token), payload=payload)
			if resp.status_code == 202:
				print('Report {} ({}) moved to Space {}'.format(self.token, self.name, space_token))
				self.space_token = space_token
			else:
				print('Report {} ({}) failed to move to Space {}'.format(self.token, self.name, space_token))

		return resp

	def update_name(self, name):
		if self.name == name:
			print('Report {} ({}) already named {}'.format(self.token, self.name, name))
		else:
			payload = {'report':{
				'name': name,
				'layout': self.layout,
				'description': self.description,
				'account_id': self.account_id,
				'space_token': self.space_token,
				'published': self.published
				}
			}

			resp = self.requester._patch('/reports/{}'.format(self.token), payload=payload)
			if resp.status_code == 202:
				print('Report {} ({}) renamed to {}'.format(self.token, self.name, name))
				self.name = name
			else:
				print('Report {} ({}) failed to rename to {}'.format(self.token, self.name, name))

		return resp

	def sync_to_github(self, commit_msg):
		payload = {'commit_message': commit_msg}
		resp = self.requester._patch('/reports/{}/sync_to_github'.format(self.token), payload=payload)
		if resp.status_code == requests.codes.ok:
			print('Report {} ({}) synced to GitHub'.format(self.token, self.name))
		else:
			print('Report {} ({}) failed to sync to GitHub'.format(self.token, self.name))

		return resp

	def disable_external_sharing(self):
		if not self.shared:
			resp = 'Skipped: External sharing already disabled for Report {} ({})'.format(self.token, self.name)
		else:
			resp = self.requester._patch('/reports/{}/external_sharing/disable'.format(self.token))
			if resp.status_code == requests.codes.ok:
				print('Success: External sharing disabled for Report {} ({})'.format(self.token, self.name))
				self.shared = False
			else:
				print('Fail: Failed to disable external sharing for Report {} ({})'.format(self.token, self.name))

		return resp

	def enable_external_sharing(self):
		if self.shared:
			resp = 'Skipped: External sharing already enabled for Report {} ({})'.format(self.token, self.name)
		else:
			resp = self.requester._patch('/reports/{}/external_sharing/enable'.format(self.token))
			if resp.status_code == requests.codes.ok:
				print('Success: External sharing enabled for Report {} ({})'.format(self.token, self.name))
				self.shared = True
			else:
				print('Fail: Failed to enable external sharing for Report {} ({})'.format(self.token, self.name))

		return resp

class ReportRun(object):

	def __init__(self, data, report_token, requester):
		self.token = data.get('token')
		self.state = data.get('state')
		self.parameters = data.get('parameters')
		self.created_at = data.get('created_at')
		self.completed_at = data.get('completed_at')
		self.python_state = data.get('python_state')
		self.form_fields = data.get('form_fields')
		self.executed_by = data.get('_links').get('executed_by').get('href')
		self.report_token = report_token

		self.requester = requester


class Query(object):

	def __init__(self, data, report_token, requester):
		self.token = data.get('token')
		self.raw_query = data.get('raw_query')
		self.created_at = data.get('created_at')
		self.name = data.get('name')
		self.last_run_id = data.get('last_run_id')
		self.data_source_id = data.get('data_source_id')
		self.report_token = report_token

		self.requester = requester

	def run(self):
		resp = self.requester._post('/reports/{}/queries/{}/runs'.format(self.report_token, self.token))
		return resp

	def delete(self):
		resp = self.requester._delete('/reports/{}/queries/{}'.format(self.report_token, self.token))
		if resp.status_code == requests.codes.ok:
			print('Query {} ({}) deleted'.format(self.token, self.name))
		else:
			print('Query {} ({}) failed to delete'.format(self.token, self.name))

		return resp

	def update_name(self, new_name):
		if self.name == new_name:
			resp = 'Skipped: Query {} already named {}'.format(self.token, self.name)
		else:
			payload = {'query':{
				'raw_query': self.raw_query,
				'name': new_name,
				'data_source_id': self.data_source_id
				}
			}

			resp = self.requester._patch('/reports/{}/queries/{}'.format(self.report_token, self.token), payload=payload)
			if resp.status_code == requests.codes.ok:
				print('Query {} ({}) renamed to {}'.format(self.token, self.name, new_name))
				self.name = new_name
			else:
				print('Query {} ({}) failed to rename to {}'.format(self.token, self.name, new_name))

		return resp

	def update_raw_query(self, raw_query):
		if self.raw_query == raw_query:
			resp = 'Skipped: Query {} already has new query'.format(self.token)
		else:
			payload = {'query':{
				'raw_query': raw_query,
				'name': self.name,
				'data_source_id': self.data_source_id
				}
			}

			resp = self.requester._patch('/reports/{}/queries/{}'.format(self.report_token, self.token), payload=payload)
			if resp.status_code == requests.codes.ok:
				print('Query {} ({}) raw query updated'.format(self.token, self.name))
				self.raw_query = raw_query
			else:
				print('Query {} ({}) failed to update raw query'.format(self.token, self.name))

		return resp


	def update_data_source(self, data_source_id):
		if self.data_source_id == data_source_id:
			resp = 'Skipped: Query {} already uses data source {}'.format(self.token. self.data_source_id)
		else:
			payload = {'query':{
				'raw_query': self.raw_query,
				'name': self.name,
				'data_source_id': data_source_id
				}
			}

			resp = self.requester._patch('/reports/{}/queries/{}'.format(self.report_token, self.token), payload=payload)
			if resp.status_code == requests.codes.ok:
				print('Query {} ({}) data source updated'.format(self.token, self.name))
				self.data_source_id = data_source_id
			else:
				print('Query {} ({}) failed to update data source'.format(self.token, self.name))

		return resp

	def get_charts(self):
		resp = self.requester._get('/reports/{}/queries/{}/charts'.format(self.report_token, self.token))
		charts = resp.get('_embedded').get('charts')
		chart_list = [Chart(chart, self.report_token, self.token, self.requester) for chart in charts]

		if resp.get('pagination'):
			while resp.get('pagination').get('page') < resp.get('pagination').get('total_pages'):
				next_page = resp.get('pagination').get('page')+1
				resp = self.requester._get('/reports/{}/queries/{}/charts?page={}'.format(self.report_token, self.token, next_page))
				charts = resp.get('_embedded').get('charts')
				for chart in charts:
					chart_instance = Chart(chart, self.report_token, self.token, self.requester)
					chart_list.append(chart_instance)

		return chart_list


class Chart(object):

	def __init__(self, data, report_token, query_token, requester):
		self.token = data.get('token')
		self.created_at = data.get('created_at')
		self.color_palatte_token = data.get('color_palette_token')
		self.report_token = report_token
		self.query_token = query_token

		self.requester = requester
