import requests


class Mode:
    BASE_URL = "https://modeanalytics.com/api"

    def __init__(self, token, password, account_name):
        self.token = token
        self.password = password
        self.account_name = account_name

    def _construct_headers(self):
        headers = requests.utils.default_headers()
        headers["User-Agent"] = "python-pymode"
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/hal+json"
        return headers

    def _get(self, url_suffix: str, params: dict = None) -> dict:
        url = self.BASE_URL + url_suffix
        headers = self._construct_headers()
        response = requests.get(
            url, auth=(self.token, self.password), headers=headers, params=params
        )
        response.raise_for_status()
        return response.json()

    def _post(self, url_suffix: str, params: dict = None, data: dict = None) -> dict:
        url = self.BASE_URL + url_suffix
        headers = self._construct_headers()
        response = requests.post(
            url,
            auth=(self.token, self.password),
            headers=headers,
            params=params,
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def _patch(self, url_suffix: str, params: dict = None, data: dict = None) -> dict:
        url = self.BASE_URL + url_suffix
        headers = self._construct_headers()
        response = requests.patch(
            url,
            auth=(self.token, self.password),
            headers=headers,
            params=params,
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def _delete(self, url_suffix: str, params: dict = None, data: dict = None) -> dict:
        url = self.BASE_URL + url_suffix
        headers = self._construct_headers()
        response = requests.delete(
            url,
            auth=(self.token, self.password),
            headers=headers,
            params=params,
            data=data,
        )
        response.raise_for_status()
        return response.json()

    def list_spaces(self) -> list:
        resp = self._get(url_suffix=f"/{self.account_name}/spaces?filter=all")
        return resp.get("_embedded").get("spaces")

    def get_space(self, space_token) -> dict:
        resp = self._get(url_suffix=f"/{self.account_name}/spaces/{space_token}")
        return resp

    def list_reports(self, space_token: str) -> list:
        page = 1
        resp = self._get(
            url_suffix=f"/{self.account_name}/spaces/{space_token}/reports?page={page}"
        )
        reports = resp.get("_embedded").get("reports")
        all_reports = reports.copy()

        # handle pagination
        while len(reports) == 30:
            page += 1
            resp = self._get(
                url_suffix=f"/{self.account_name}/spaces/{space_token}/reports?page={page}"
            )
            reports = resp.get("_embedded").get("reports")
            all_reports.extend(reports)

        return all_reports

    def get_report(self, report_token: str) -> dict:
        resp = self._get(url_suffix=f"/{self.account_name}/reports/{report_token}")
        return resp

    def archive_report(self, report_token: str):
        resp = self._patch(
            url_suffix=f"/{self.account_name}/reports/{report_token}/archive"
        )
        return resp

    def unarchive_report(self, report_token: str):
        resp = self._patch(
            url_suffix=f"/{self.account_name}/reports/{report_token}/unarchive"
        )
        return resp

    def list_memberships(self) -> list:
        resp = self._get(url_suffix=f"/{self.account_name}/memberships")
        return resp.get("_embedded").get("memberships")

    def get_membership(self, membership_token: str) -> dict:
        resp = self._get(
            url_suffix=f"/{self.account_name}/memberships/{membership_token}"
        )
        return resp

    def delete_membership(self, membership_token: str) -> dict:
        resp = self._delete(
            url_suffix=f"/{self.account_name}/memberships/{membership_token}"
        )
        return resp

    def get_user(self, username: str) -> dict:
        resp = self._get(url_suffix=f"/{username}")
        return resp
