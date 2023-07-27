from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from unittest.mock import ANY

from .models import ToDo


class TestToDo(APITestCase):

    def setUp(self) -> None:
        self.user_1, created = User.objects.update_or_create(username="User 1")
        self.user_2, created = User.objects.update_or_create(username="User 2")

    def test_unauthenticated(self):

        response = self.client.get("/api/todo")
        self.assertEqual(response.status_code, 403)

        response = self.client.post("/api/todo")
        self.assertEqual(response.status_code, 403)

        response = self.client.post("/api/todo/mark_complete/1")
        self.assertEqual(response.status_code, 403)

        response = self.client.delete("/api/todo/1")
        self.assertEqual(response.status_code, 403)

    def test_create_todo_missing_title(self):

        self.client.force_authenticate(user=self.user_1)
        response = self.client.post("/api/todo", {"description": "This is todo 1"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_todo_valid(self):

        self.client.force_authenticate(user=self.user_1)
        response = self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/todo")
        self.assertEqual(len(response.json()), 1)
        self.assertDictEqual(response.json()[0], {"id": ANY, "created_at": ANY, "updated_at": ANY, "title": 'ToDo 1',
                                                  "description": 'This is todo 1', "completed": False, "user": 1})

    def test_create_todos_valid(self):

        # user 1 todos
        self.client.force_authenticate(user=self.user_1)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # user 2 todos
        self.client.force_authenticate(user=self.user_2)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # There should be 4 todos in db
        self.assertEqual(ToDo.objects.all().count(), 4)

        # User 1 get request should get 2 todos
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get("/api/todo")
        self.assertEqual(len(response.json()), 2)

    def test_delete_todos(self):

        # user 1 todos
        self.client.force_authenticate(user=self.user_1)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # user 2 todos
        self.client.force_authenticate(user=self.user_2)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # user 2 tried to delete user 1 item
        user_1_todos = ToDo.objects.filter(user=self.user_1)
        response = self.client.delete(f"/api/todo/{user_1_todos[0].id}")   # User 2 tried to delete user 1 item
        self.assertEqual(response.status_code, 404)

        # user 1 delete his own item
        self.client.force_authenticate(user=self.user_1)
        id = user_1_todos[0].id
        response = self.client.delete(f"/api/todo/{id}")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"/api/todo/{id}")
        self.assertEqual(response.status_code, 404)

    def test_mark_complete(self):

        # user 1 todos
        self.client.force_authenticate(user=self.user_1)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # user 2 todos
        self.client.force_authenticate(user=self.user_2)
        self.client.post("/api/todo", {"title": "ToDo 1", "description": "This is todo 1"}, format="json")
        self.client.post("/api/todo", {"title": "ToDo 2", "description": "This is todo 2"}, format="json")

        # user 2 tried to mark complete user 1 item
        user_1_todos = ToDo.objects.filter(user=self.user_1)
        response = self.client.post(f"/api/todo/mark_complete/{user_1_todos[0].id}")   # User 2 tried to delete user 1 item
        self.assertEqual(response.status_code, 404)

        # user 1 mark complete his own item
        self.client.force_authenticate(user=self.user_1)
        id = user_1_todos[0].id
        # False before mark complete
        response = self.client.get(f"/api/todo/{id}")
        self.assertEqual(response.json()["completed"], False)
        # mark complete
        response = self.client.post(f"/api/todo/mark_complete/{id}")
        self.assertEqual(response.status_code, 202)
        response = self.client.get(f"/api/todo/{id}")
        self.assertEqual(response.json()["completed"], True)
        # no error if mark again
        response = self.client.post(f"/api/todo/mark_complete/{id}")
        self.assertEqual(response.status_code, 202)
