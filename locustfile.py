import time
from locust import HttpUser, TaskSet, events, task, between


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("Test started!")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("Test has ended!")


class SchemaSection(TaskSet):
    login_token = ''
    wait_time = between(2, 7)

    @task(10)
    def schema_list(self):
        self.client.get("")

    @task
    def schema_detail(self):
        for id in range(20):
            self.client.get(f"{id + 1}/detail", name="{id}/detail")
            time.sleep(5)


class ListSchemaUser(HttpUser):
    wait_time = between(5, 10)
    tasks = [SchemaSection]
    login_token = ''

    def on_start(self):
        response = self.client.post(
            "api-token-auth/",
            json={"username": "admin", "password": "admin"}
        )
        self.login_token = response.json()['token']
