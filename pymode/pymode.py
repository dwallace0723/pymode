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
		memberships = [Membership(membership) for membership in memberships]

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

	def get_report(self, report_token):
		resp = self.requester._get('/reports/{}'.format(report_token))
		return Report(resp, self.requester)

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

		return spaces_list

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

		return report_list

class Membership(object):

	def __init__(self, data, requester):
		self.token = data.get('_links').get('self').get('href')
		self.user = data.get('_links').get('self').get('user')
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

		self.requester = requester

	def run(self):
		resp = self.requester._post('/reports/{}/runs'.format(self.token))
		if resp.status_code == 202:
			print('Report {} ({}) run queued'.format(self.token, self.name))
		else:
			print('Report Run Failed')

		return resp

	def archive(self):
		resp = self.requester._patch('/reports/{}/archive'.format(self.token))
		if resp.status_code == requests.codes.ok:
			print('Report {} ({}) archived'.format(self.token, self.name))
		else:
			print('Report {} ({}) failed to archive'.format(self.token, self.name))

		return resp

	def unarchive(self):
		resp = self.requester._patch('/reports/{}/unarchive'.format(self.token))
		if resp.status_code == requests.codes.ok:
			print('Report {} ({}) unarchived'.format(self.token, self.name))
		else:
			print('Report {} ({}) failed to unarchive'.format(self.token, self.name))

		return resp

	def get_queries(self):
		resp = self.requester._get('/reports/{}/queries'.format(self.token))
		queries = resp.get('_embedded').get('queries')
		query_list = [Query(query, self.token, self.requester) for query in queries]

		return query_list


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
		return resp

	def update_name(self, new_name):
		values = {"query":{"name":{"value":new_name}}}
		resp = self.requester._patch(url_suffix='/reports/{}/queries/{}'.format(self.report_token, self.token), payload=values)
		return resp
