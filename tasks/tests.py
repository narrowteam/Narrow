from django.test import TestCase
from rest_framework.test import APITestCase
from UserManagement.models import User
from projects.models import Project
from .models import Task, TaskPermission
from django.db.models import Q
from django.urls import reverse
from rest_framework import status


# class TaskModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(email='test_email@gmail.com',
#                                         first_name='aDam',
#                                         last_name='Smith',
#                                         password='123'
#                                         )

class TaskViewTestCase(APITestCase):

    def setUp(self):
        self.test_data = {
            'email': 'test@gmail.com',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        self.test_user_1 = User.objects.create(
            email='test@gmail.com',
            password='Ac54!ftggre',
            first_name='Adam',
            last_name='Smith'
        )
        self.test_user_2 = User.objects.create(
            email='test1@gmail.com',
            password='Ac54!ftggre',
            first_name='Tom',
            last_name='Smith'
        )
        self.test_project = Project.objects.create(
            owner=self.test_user_1,
            project_name="TestName",
            description="some description"
        )
        self.test_project_main_task = Task.objects.get(
            project=self.test_project,
            is_main=True
        )

    def test_pushing_sub_task(self):
        url = reverse('tasks:task-detail', args=[self.test_project_main_task.id]) + 'push_sub_task/'
        dataset = {
            'name': "test_task_1",
            'description': "test_task_desc"
        }
        self.client.force_authenticate(self.test_user_1)
        response = self.client.post(url, data=dataset)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('name' in response.data)
        self.assertTrue('description' in response.data)

