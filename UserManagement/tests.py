from django.test import TestCase
from UserManagement.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from UserManagement import views


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='123'
                                        )


    def _get_initial_user_data(self):
        return {
            'email': 'test_email@gmail.com',
            'first_name': 'Adam',
            'last_name': 'Smith',
            'password': '123'
        }

    def test_full_name(self):
        user = self.user
        self.assertEqual(user.get_full_name(), 'Adam Smith')

    def test_update(self):
        new_data = {
            'email': 'test_email2@gmail.pl',
            'first_name': 'Tom',
            'last_name':  'Jerry',
        }
        user = self.user
        user.update_user(**new_data)
        self.assertEqual(user.first_name, 'Tom')
        self.assertEqual(user.email, 'test_email2@gmail.pl')
        self.assertEqual(user.last_name, 'Jerry')
        self.assertTrue(user.check_password('123'))



class UserViewSet(APITestCase):

    def setUp(self):
        self.test_data = {
            'email': 'test@gmail.com',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        self.other_test_data = {
            'email': 'test1@gmail.com',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        self.test_user = User.objects.create(**self.test_data)

    def test_create_positive_create_test(self):
        url = '/user/'
        response = self.client.post(url, self.other_test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.other_test_data["email"])

    def test_create_fail_not_unique_email(self):
        url = '/user/'
        response = self.client.post(url, self.test_data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_fail_invalid_password(self):
        url = '/user/'
        test_data_invaild_password = {
            'email': 'test_inv_pass@gmail.com',
            'password': '123',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        response = self.client.post(url, )
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
    def test_create_fail_invaild_email(self):
        url = '/user/'
        data = {
            'email': '3_test',
            'password': 'Ac54!ftggre',
            'first_name': 'Adam',
            "last_name": 'Smith'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"email": ["Enter a valid email address."]})

    def test_create_fail_not_required_data(self):
        url = '/user/'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data, {"email": ["This field is required."],
                                         "first_name": ["This field is required."],
                                         "last_name": ["This field is required."],
                                         "password": ["This field is required."]
                                         })
    #
    # def test_patch_positive(self):
    #     url1 = '/user/'
    #     data = {
    #         'settings': {
    #             'email_notifications_on_events': True
    #         }
    #     }
    #     self.client.force_authenticate(user=self.test_user)
    #     response = self.client.patch(url1, data)
    #     user = User.objects.get(email='3_test@gm.pl')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(user.settings.email_notifications_on_events, True)

    def test_set_password_positive(self):
        url = '/user/set_password/'
        data = {
            'current_password': self.test_data['password'],
            'new_password': "xD123@1!a"
        }
        self.client.force_authenticate(user=self.test_user)
        reponse = self.client.post(url, data)
        self.assertEqual(reponse.status_code, status.HTTP_200_OK)
        self.assertTrue(self.test_user.check_password("xD123@1!a"))

    def test_set_password__fail_invalid_current_password(self):
        url = '/user/set_password/'
        data = {
            'current_password': self.test_data['password'] + 'a',
            'new_password': "xD123@1!a"
        }
        self.client.force_authenticate(user=self.test_user)
        reponse = self.client.post(url, data)

        self.assertEqual(reponse.status_code, status.HTTP_406_NOT_ACCEPTABLE)

