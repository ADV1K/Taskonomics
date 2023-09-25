from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from base.models import Project, Task, User

SIGNUP_URL = "/api/v1/signup/"
LOGIN_URL = "/api/v1/login/"
REFRESH_TOKEN_URL = "/api/v1/login/refresh/"
PROJECT_CREATE_URL = "/api/v1/project/"
PROJECT_DETAIL_URL = "/api/v1/project/{id}/"
TASK_CREATE_URL = "/api/v1/task/"
TASK_DETAIL_URL = "/api/v1/task/{id}/"


class TestAuth(APITestCase):
    def test_auth(self):
        # Test signup
        response = self.client.post(
            SIGNUP_URL,
            {"username": "testuser", "password": "testpassword", "timezone": "Asia/Kolkata"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="testuser").timezone, "Asia/Kolkata")

        # Test correct login
        response = self.client.post(
            LOGIN_URL,
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.refresh_token = response.data["refresh"]
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        # Test wrong login
        response = self.client.post(
            LOGIN_URL,
            {"username": "testuser", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

        # Test Refresh Token
        response = self.client.post(
            REFRESH_TOKEN_URL,
            {"refresh": self.refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)


class TestProject(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.headers = {"Authorization": f"Bearer {AccessToken.for_user(user)}"}

    def test_project(self):
        # Create Project
        response = self.client.post(
            PROJECT_CREATE_URL,
            {"name": "testproject"},
            headers=self.headers,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), 1)

        # Get Project
        response = self.client.get(PROJECT_CREATE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "testproject")

        # Get Project Detail
        response = self.client.get(PROJECT_DETAIL_URL.format(id=1), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "testproject")

        # Update Project
        response = self.client.put(
            PROJECT_DETAIL_URL.format(id=1),
            {"name": "testproject2"},
            headers=self.headers,
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "testproject2")

        # Delete Project
        response = self.client.delete(PROJECT_DETAIL_URL.format(id=1), headers=self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.count(), 0)


class TestTask(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        Project.objects.create(name="testproject", owner=user)
        self.headers = {"Authorization": f"Bearer {AccessToken.for_user(user)}"}

    def test_task(self):
        # Create Task
        response = self.client.post(
            TASK_CREATE_URL,
            {"name": "testtask", "project": 1, "assignee": 1, "reviewers": [1]},
            headers=self.headers,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)

        # Get Task
        response = self.client.get(TASK_CREATE_URL, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "testtask")

        # Get Task Detail
        response = self.client.get(TASK_DETAIL_URL.format(id=1), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "testtask")

        # Update Task
        # response = self.client.put(
        #     TASK_DETAIL_URL.format(id=1),
        #     {"name": "testtask2"},
        #     headers=self.headers,
        #     format="json",
        # )
        # print(response.data)
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data["name"], "testtask2")

        # Delete Task
        response = self.client.delete(TASK_DETAIL_URL.format(id=1), headers=self.headers)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 0)
