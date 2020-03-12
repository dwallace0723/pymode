import platform
import sys
from typing import Any, ClassVar, Dict, Optional

import attr
import requests

from .version import __version__


@attr.s
class Mode(object):
    _base_url: ClassVar[str] = "https://app.mode.com/api"

    _organization: str = attr.ib()
    _token: str = attr.ib(repr=False)
    _password: str = attr.ib(repr=False)
    _url: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._url = f"{self._base_url}/{self._organization}"

    @property
    def organization(self):
        return self._organization

    @property
    def token(self):
        return self._token

    @property
    def base_url(self):
        return self._base_url

    @property
    def url(self):
        return self._url

    def _construct_user_agent(self) -> str:
        client = f"pymode/{__version__}"
        python_version = f"Python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        system_info = f"{platform.system()}/{platform.release()}"
        user_agent = " ".join([python_version, client, system_info])
        return user_agent

    def _construct_headers(self) -> Dict:
        """Constructs a standard set of headers for HTTP requests."""
        headers = requests.utils.default_headers()
        headers["User-Agent"] = self._construct_user_agent()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/hal+json"
        return headers

    def _request(
        self, *, method: str, url: str, params: Optional[Dict] = None, json: Optional[Dict] = None
    ) -> requests.Response:
        headers = self._construct_headers()
        response = requests.request(
            method=method, url=url, auth=(self._token, self._password), headers=headers, params=params, json=json
        )
        response.raise_for_status()
        return response

    def _get_resource(self, *, resource: str, params: Optional[Dict] = None) -> requests.Response:
        url = f"{self.url}/{resource}"
        resp = self._request(method="GET", url=url, params=params)
        return resp

    def _post_resource(
        self, *, resource: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict] = None,
    ) -> requests.Response:
        url = f"{self.url}/{resource}"
        resp = self._request(method="POST", url=url, params=params, json=json)
        return resp

    def _put_resource(
        self, *, resource: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict] = None,
    ) -> requests.Response:
        url = f"{self.url}/{resource}"
        resp = self._request(method="PUT", url=url, params=params, json=json)
        return resp

    def _patch_resource(
        self, *, resource: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict] = None,
    ) -> requests.Response:
        url = f"{self.url}/{resource}"
        resp = self._request(method="PATCH", url=url, params=params, json=json)
        return resp

    def _delete_resource(
        self, *, resource: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict] = None,
    ) -> requests.Response:
        url = f"{self.url}/{resource}"
        resp = self._request(method="DELETE", url=url, params=params, json=json)
        return resp

    def list_spaces(self, **kwargs) -> requests.Response:
        resp = self._get_resource(resource="spaces", params=kwargs)
        return resp

    def get_space(self, *, space_token: str, **kwargs) -> requests.Response:
        resp = self._get_resource(resource=f"spaces/{space_token}", params=kwargs)
        return resp

    def create_space(self, *, space_type: str, name: str, description: Optional[str] = None) -> requests.Response:
        data = {"space": {"space_type": space_type, "name": name}}

        if description is not None:
            data["space"]["description"] = description

        resp = self._post_resource(resource="spaces", json=data)
        return resp

    def update_space(
        self, *, space_token: str, space_type: str, name: str, description: Optional[str] = None
    ) -> requests.Response:
        data = {"space": {"space_type": space_type, "name": name}}

        if description is not None:
            data["space"]["description"] = description

        resp = self._post_resource(resource=f"spaces/{space_token}", json=data)
        return resp

    def delete_space(self, *, space_token: str) -> requests.Response:
        resp = self._delete_resource(resource=f"spaces/{space_token}")
        return resp

    def list_memberships(self, **kwargs) -> requests.Response:
        "Retrieves all Memberships within an Organization."
        resp = self._get_resource(resource="memberships", params=kwargs)
        return resp

    def get_membership(self, *, membership_token: str, **kwargs) -> requests.Response:
        "Retrieves a specific Membership within an Organization."
        resp = self._get_resource(resource=f"memberships/{membership_token}", params=kwargs)
        return resp

    def delete_membership(self, *, membership_token: str) -> requests.Response:
        "Deletes a Membership within an Organization."
        resp = self._delete_resource(resource=f"memberships/{membership_token}")
        return resp

    def create_invite(self, *, invitee_email: str, message: str) -> requests.Response:
        "Creates an Invite to join an Organization."
        data = {"invite": {"invitee": {"email": invitee_email,}, "message": message}}

        resp = self._post_resource(resource="invites", json=data)
        return resp

    def list_space_memberships(self, *, space_token: str, **kwargs) -> requests.Response:
        "Retrieves all Memberships to a Space within an Organization."
        resp = self._get_resource(resource=f"spaces/{space_token}/memberships", params=kwargs)
        return resp

    def get_space_membership(self, *, space_token: str, space_membership_token: str, **kwargs) -> requests.Response:
        "Retrieves a specific Space Membership within an Organization."
        resp = self._get_resource(resource=f"spaces/{space_token}/memberships/{space_membership_token}", params=kwargs)
        return resp

    def create_space_membership(self, *, space_token: str, member_type: str, member_token: str) -> requests.Response:
        "Creates a Space Membership within an Organization."
        if member_type not in ["User", "UserGroup"]:
            raise ValueError("Parameter 'member_type' must be either 'User' or 'UserGroup'.")

        data = {"membership": {"member_type": member_type, "member_token": member_token}}

        resp = self._post_resource(resource=f"spaces/{space_token}/memberships", json=data)
        return resp

    def delete_space_membership(self, *, space_token: str, membership_token: str) -> requests.Response:
        "Deletes a Space Membership within an Organization."
        resp = self._delete_resource(resource=f"spaces/{space_token}/memberships/{membership_token}")
        return resp

    def list_reports(self, *, space_token: str, **kwargs) -> requests.Response:
        "Retrieves all Reports in a Space within an Organization."
        resp = self._get_resource(resource=f"spaces/{space_token}/reports", params=kwargs)
        return resp

    def get_report(self, *, report_token: str, **kwargs) -> requests.Response:
        "Retrieves a specific Report within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}", params=kwargs)
        return resp

    def update_report(self, *, report_token: str, **kwargs) -> requests.Response:
        "Updates a Report within an Organization."
        data = {"report": kwargs}
        resp = self._patch_resource(resource=f"reports/{report_token}", json=data)
        return resp

    def delete_report(self, *, report_token: str) -> requests.Response:
        "Deletes a Report within an Organization."
        resp = self._delete_resource(resource=f"reports/{report_token}")
        return resp

    def archive_report(self, *, report_token: str) -> requests.Response:
        "Archives a Report within an Organization."
        resp = self._patch_resource(resource=f"reports/{report_token}/archive")
        return resp

    def unarchive_report(self, *, report_token: str) -> requests.Response:
        "Unarchives a Report within an Organization."
        resp = self._patch_resource(resource=f"reports/{report_token}/unarchive")
        return resp

    def list_report_runs(self, *, report_token: str, **kwargs) -> requests.Response:
        "Retrieves all Report Runs for a specific Report within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}/runs", params=kwargs)
        return resp

    def get_report_run(self, *, report_token: str, report_run_token: str, **kwargs) -> requests.Response:
        "Retrieves a specific Report Run within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}/runs/{report_run_token}", params=kwargs)
        return resp

    def clone_report_run(self, *, report_token: str, report_run_token: str) -> requests.Response:
        "Clones a specific Report Run within an Organization."
        resp = self._post_resource(resource=f"reports/{report_token}/runs/{report_run_token}/clone")
        return resp

    def create_report_run(self, *, report_token: str, **kwargs) -> requests.Response:
        "Creates a Rpeort Run for a specific Report within an Organization."
        data = {"parameters": kwargs}
        resp = self._post_resource(resource=f"reports/{report_token}/runs", json=data)
        return resp

    def list_queries(self, *, report_token: str, **kwargs) -> requests.Response:
        "Retrieves all Queries in a specific Report within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}/queries", params=kwargs)
        return resp

    def get_query(self, *, report_token: str, query_token: str, **kwargs) -> requests.Response:
        "Retrieves a specific Query within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}/queries/{query_token}", params=kwargs)
        return resp

    def create_query(self, *, report_token: str, data_source_id: str, raw_query: str, **kwargs) -> requests.Response:
        "Creates a Query within a specific Report within an Organization."
        data = {"query": {"raw_query": raw_query, "data_source_id": data_source_id}}

        if kwargs:
            data["query"].update(kwargs)

        resp = self._post_resource(resource=f"reports/{report_token}/queries", json=data)
        return resp

    def update_query(self, *, report_token: str, query_token: str, **kwargs) -> requests.Response:
        "Updates a Query within an Organization."
        data = {"query": {kwargs}}
        resp = self._patch_resource(resource=f"reports/{report_token}/queries/{query_token}", json=data)
        return resp

    def delete_query(self, *, report_token: str, query_token: str) -> requests.Response:
        "Deletes a Query within an Organization."
        resp = self._delete_resource(resource=f"reports/{report_token}/queries/{query_token}")
        return resp

    def list_query_runs(self, *, report_token: str, report_run_token: str, **kwargs) -> requests.Response:
        "Retrieves all Query Runs in a specific Report Run within an Organization."
        resp = self._get_resource(resource=f"reports/{report_token}/runs/{report_run_token}/query_runs", params=kwargs)
        return resp

    def get_query_run(
        self, *, report_token: str, report_run_token: str, query_run_token: str, **kwargs
    ) -> requests.Response:
        "Retrieves a specific Query Run within an Organization."
        resp = self._get_resource(
            resource=f"reports/{report_token}/runs/{report_run_token}/query_runs/{query_run_token}", params=kwargs
        )
        return resp

    def get_query_run_results(
        self, *, report_token: str, report_run_token: str, query_run_token: str, file_type: str, **kwargs
    ) -> requests.Response:
        "Retrieves the result set for specific Query Run within an Organization."

        if file_type not in ["csv", "json"]:
            raise ValueError("Parameter 'file_type' must be either 'csv' or 'json'.")

        resp = self._get_resource(
            resource=f"reports/{report_token}/runs/{report_run_token}/query_runs/{query_run_token}/results/content.{file_type}",
            params=kwargs,
        )
        return resp

    def get_report_run_results(
        self, *, report_token: str, report_run_token: str, file_type: str, **kwargs
    ) -> requests.Response:
        "Retrieves the result set for specific Report Run within an Organization."

        if file_type not in ["csv", "json"]:
            raise ValueError("Parameter 'file_type' must be either 'csv' or 'json'.")

        resp = self._get_resource(
            resource=f"reports/{report_token}/runs/{report_run_token}/results/content.{file_type}", params=kwargs
        )
        return resp

    def get_report_run_pdf(self, *, report_token: str, report_run_token: str, **kwargs) -> requests.Response:
        "Retrieves the result set for specific Report Run within an Organization."

        resp = self._get_resource(
            resource=f"reports/{report_token}/exports/runs/{report_run_token}/format/download", params=kwargs
        )
        return resp
