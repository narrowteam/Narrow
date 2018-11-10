from django.test import TestCase
from UserManagement.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from UserManagement import views


class UserModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='123'
                                        )

        self.assertEqual(user.first_name, 'Adam')
        self.assertEqual(user.email, 'test_email@gmail.com')
        self.assertEqual(user.last_name, 'Smith')
        self.assertTrue(user.check_password('123'))

    def get_user(self):
        return User.objects.get(email='test_email@gmail.com')

    def _get_initial_user_data(self):
        return {
            'email': 'test_email@gmail.com',
            'first_name': 'Adam',
            'last_name': 'Smith',
            'password': '123'
        }

    def test_full_name(self):
        user = self.get_user()
        self.assertEqual(user.get_full_name(), 'Adam Smith')

    def test_update(self):
        new_data = {
            'email': 'test_email2@gmail.pl',
            'first_name': 'Tom',
            'last_name':  'Jerry',
            'password': '1234',
        }
        user = self.get_user()
        user.update_user(**new_data)
        self.assertEqual(user.first_name, 'Tom')
        self.assertEqual(user.email, 'test_email2@gmail.pl')
        self.assertEqual(user.last_name, 'Jerry')
        self.assertTrue(user.check_password('1234'))
        user.update_user(**self._get_initial_user_data())



class UserViewSet(APITestCase):

    def setUp(self):
        self.test_data = {
            'email': 'test@gmail.com',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        self.test_data_broken_pa = {
            'email': '3_test@gmail.com',
            'password': '123',
            'first_name': 'Adam',
            "last_name": 'Smith'
                }



    def test_create_positive_create_test(self):
        url = '/user/'
        response = self.client.post(url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_fail_not_unique_email(self):
    #     url = '/user/'
    #     response = self.client.post(url, self.test_data)
    #     self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_fail_password_not_validated(self):
        url = '/user/'
        response = self.client.post(url, self.test_data_broken_pa)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"password":["This password is too short. It must contain at least 8 characters.","This password is too common.","This password is entirely numeric."]})

    def test_create_fail_email_not_validated(self):
        url = '/user/'
        data = {
            'email': '3_test',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
                }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"email":["Enter a valid email address."]})

    def test_create_fail_not_required_data(self):
        url = '/user/'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"email":["This field is required."],"first_name":["This field is required."],"last_name":["This field is required."],"password":["This field is required."]})

    def test_create_positve(self):
        url1 = '/user/'
        data1 = {
            'email': '3_test@gm.pl',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        response = self.client.post(url1, data1)
        url2 = '/user/1/'
        data2 = {
            'email': '4_test@gm.pl',
            'password': 'Ac54!ftggre',
            'first_name': 'Adamm',
            "last_name": 'Smithm'
        }
        user = User.objects.get(email='3_test@gm.pl')
        self.client.force_authenticate(user=user)
        response = self.client.patch(url2, data2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_negative_validation_error(self):
        url1 = '/user/'
        data1 = {
            'email': '3_test@gm.pl',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        response = self.client.post(url1, data1)
        user = User.objects.get(email='3_test@gm.pl')

        url2 = '/user/%s/' %str(user.id)
        data2 = {
            'email': '4_test',
            'password': '123',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        self.client.force_authenticate(user=user)
        response = self.client.patch(url2, data2)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"email":["Enter a valid email address."], "password":["This password is too short. It must contain at least 8 characters.","This password is too common.","This password is entirely numeric."]})
