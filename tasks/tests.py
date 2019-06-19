from django.test import TestCase
from rest_framework.test import APITestCase
from UserManagement.models import User
from projects.models import Project
from .models import Task
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
        self.test_user_1_proj_owner = User.objects.create(
            email='test@gmail.com',
            password='Ac54!ftggre',
            first_name='Adam',
            last_name='Smith'
        )
        self.test_user_2_proj_participatnt = User.objects.create(
            email='test1@gmail.com',
            password='Ac54!ftggre',
            first_name='Tom',
            last_name='Smith'
        )
        self.test_user_3_random_user = User.objects.create(
            email='test2@gmail.com',
            password='Ac54!ftggre',
            first_name='Tom',
            last_name='Smith'
        )
        self.test_project = Project.objects.create(
            owner=self.test_user_1_proj_owner,
            project_name="TestName",
            description="some description"
        )
        self.test_project.add_participant(self.test_user_2_proj_participatnt)


    def test_adding_task(self):
        url = f'/projects/project_tasks/{self.test_project.id}/tasks/'
        dataset = {
            'name': "test_task_1",
            'description': "test_task_desc"
        }
        self.client.force_authenticate(self.test_user_1_proj_owner)
        response = self.client.post(url, data=dataset)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(id=response.data['id']).exists())

    def test_adding_task_failed_404(self):
        url = f'projects/project_tasks/100000000000/tasks/'
        dataset = {
            'name': "test_task_1",
            'description': "test_task_desc"
        }
        self.client.force_authenticate(self.test_user_1_proj_owner)
        resp = self.client.post(url, data=dataset)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_adding_task_failed_unauthorized_participant(self):
        url = f'projects/project_tasks/{self.test_project.id}/tasks/'
        dataset = {
            'name': "test_task_1",
            'description': "test_task_desc"
        }
        self.client.force_authenticate(self.test_user_2_proj_participatnt)
        resp = self.client.post(url, data=dataset)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_adding_task_failed_unauthorized_random(self):
        url = f'projects/project_tasks/{self.test_project.id}/tasks/'
        dataset = {
            'name': "test_task_1",
            'description': "test_task_desc"
        }
        self.client.force_authenticate(self.test_user_3_random_user)
        resp = self.client.post(url, data=dataset)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)



    # def test_pushing_sub_task(self):
    #     url = f'/projects/project_tasks/{self.test_project.id}/'
    #     dataset = {
    #         'name': "test_task_1",
    #         'description': "test_task_desc"
    #     }
    #     self.client.force_authenticate(self.test_user_1)
    #     response = self.client.post(url, data=dataset)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue('name' in response.data)
    #     self.assertTrue('description' in response.data)

