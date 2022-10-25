import time
from locust import HttpUser, task, between
from http import HTTPStatus

FULL_URL = "/api/v1/members?gn=hinatazaka"
API_KEY = "key=xxx"


class APIAccess(HttpUser):
    @task
    def with_apikey(self):
        self.client.get(f"{FULL_URL}&{API_KEY}")

    @task
    def without_apikey(self):
        with self.client.get(FULL_URL, catch_response=True) as response:
            # status code 403 is expected.
            if response.status_code == HTTPStatus.FORBIDDEN:
                response.success()
