from django.test import TestCase
from UserManagement.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from UserManagement import views
from projects.models import Project, ProjectInvitation
from UserManagement.models import User
from django.db.models import Q

class ProjectTest(TestCase):
    def setUp(self):
        self.user_owner = User.objects.create(email='test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='!*&!*(HN'
                                        )
        self.user_to_operations = User.objects.create(email='2test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='!*&!*(HN'
                                        )
        self.dataset={
            'project_name': 'test',
            'owner': self.user_owner
        }

        self.project = Project.objects.create(**self.dataset)


    def test_create_project(self):
        proj = Project.objects.create(**self.dataset)
        self.assertEqual(proj.project_name,'test')
        self.assertEqual(proj.owner, self.user_owner)

    def add_participant(self):
        self.project.add_participant(self.user_to_operations)
        self.assertTrue(self.user_to_operations in self.project.participants)
        self.project.participants.remove(self.user_to_operations)

    def remove_participants(self):
        self.project.add(self.user_to_operations)
        self.project.remove_participants([self.user_to_operations])
        self.assertTrue(self.user_to_operations not in self.project)

class InvitationTest(TestCase):
    def setUp(self):
        self.user_owner = User.objects.create(email='test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='!*&!*(HN'
                                        )
        self.user_to_operations = User.objects.create(email='2test_email@gmail.com',
                                        first_name='aDam',
                                        last_name='Smith',
                                        password='!*&!*(HN'
                                        )
        self.dataset={
            'project_name': 'test',
            'owner': self.user_owner
        }
        self.project = Project.objects.create(**self.dataset)

    def test_remove_with_duplicates(self):
        inv1 = ProjectInvitation(
            owner= self.user_owner,
            project=self.project
        )
        inv2 = ProjectInvitation(
            owner=self.user_owner,
            project=self.project
        )
        inv1.delete_with_duplicates()
        self.assertFalse(ProjectInvitation.objects.filter(
            Q(owner=self.user_owner) & Q(project=self.project)
        ).exists())

class ProjectViewSetTest(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create(email='test_email@gmail.com',
                                                   first_name='aDam',
                                                   last_name='Smith',
                                                   password='!*&!*(HN'
                                                   )
        self.user_to_operations = User.objects.create(email='2test_email@gmail.com',
                                                           first_name='aDam',
                                                           last_name='Smith',
                                                           password='!*&!*(HN'
                                                           )
        self.user_to_operations2 = User.objects.create(email='test_inv2_email@gmail.com',
                                                        first_name='aDam',
                                                        last_name='Smith',
                                                        password='!*&!*(HN'
                                                        )
        self.user_not_owner = User.objects.create(email='3test_email@gmail.com',
                                                           first_name='aDam',
                                                           last_name='Smith',
                                                           password='!*&!*(HN'
                                                           )


        self.dataset = {
            'project_name': 'test',
            'owner': self.user_owner
        }
        self.dataset_wrong = {}
        self.project = Project.objects.create(
            project_name='test',
            owner=self.user_owner
        )

        self.project_to_delete = Project.objects.create(**self.dataset)
        self.project_to_update = Project.objects.create(**self.dataset)

        self.url_detail_project = reverse('projects:project-detail', args=[self.project.id])
        self.url_list_project = reverse('projects:project-list')


    def test_project_creation(self):
        url = reverse('projects:project-list')
        self.client.force_authenticate(user=self.user_owner)
        dataset = {
            'project_name': 'test',
        }
        resp = self.client.post(url, dataset)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_fail_project_creation(self):
        url = reverse('projects:project-list')
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.post(url, self.dataset_wrong)
        self.assertEqual(resp.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_project_delete(self):
        proj_id = self.project_to_delete.id
        url = reverse('projects:project-detail', args=[str(proj_id)])
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(Project.objects.filter(pk=proj_id).exists())

    def test_project_delete_fail_auth_unauthorized(self):
        proj_id = self.project_to_delete.id
        url = reverse('projects:project-detail', args=[str(proj_id)])
        self.client.force_authenticate(user=self.user_not_owner)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_project_get(self):
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.get(self.url_detail_project)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('participants' in resp.data,)
        self.assertTrue('owner' in resp.data,)
        self.assertTrue('id' in resp.data,)
        self.assertTrue('project_name' in resp.data,)
        self.assertTrue('project_name' in resp.data,)
        self.assertTrue('description' in resp.data,)

    def test_project_get_404(self):
        url = reverse('projects:project-detail', args=[10000000])
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_get_fail_auth_unauthorized(self):
        self.client.force_authenticate(user=self.user_not_owner)
        resp = self.client.get(self.url_detail_project)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_list(self):
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.get(self.url_list_project)
        self.assertTrue('id' in resp.data[0])
        self.assertTrue('owner' in resp.data[0])
        self.assertTrue('project_name' in resp.data[0])
        self.assertTrue('description' in resp.data[0])
        self.assertTrue('participants__count' in resp.data[0])
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self._list_are_owner_of_all(resp.data, self.user_owner))

    def _list_are_owner_of_all(self,list , user):
        for x in list:
            if x['owner']['id'] != user.id: return False
        return True

    def test_partial_update(self):
        url = reverse('projects:project-detail', args=[self.project_to_update.id])
        self.client.force_authenticate(user=self.user_owner)
        data ={
            'project_name': 'test_update',
            'description': 'test_update'
        }
        resp = self.client.patch(url, data)
        updated_proj = Project.objects.get(pk=self.project_to_update.id)
        self.assertEqual(updated_proj.project_name, 'test_update')
        self.assertEqual(updated_proj.description, 'test_update')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_partial_update_404(self):
        url = reverse('projects:project-detail', args=[10000000])
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_patch_fail_auth_unauthorized(self):
        url = reverse('projects:project-detail', args=[self.project_to_update.id])
        self.client.force_authenticate(user=self.user_not_owner)
        resp = self.client.patch(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_users(self):
        url = reverse('projects:project-detail', args=[self.project_to_update.id]) +'invite/'
        data ={'invitations_list':[
                {'id': self.user_to_operations.id},
                {'email': self.user_to_operations2.email}
            ]}
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.post(url,data)
        updated_proj = Project.objects.get(pk=self.project_to_update.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(ProjectInvitation.objects.filter(Q(owner=self.user_to_operations) & Q(project=updated_proj)).exists())
        self.assertTrue(ProjectInvitation.objects.filter(Q(owner=self.user_to_operations2) & Q(project=updated_proj)).exists())

    def test_invite_404(self):
        url = reverse('projects:project-detail', args=[self.project.id]) + 'invite/'
        data = {'invitations_list': [
            {'id': self.user_to_operations.id},
        ]}
        url = reverse('projects:project-detail', args=[1000000]) + 'invite/'
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_project_invite_fail_auth_unauthorized(self):
        url = reverse('projects:project-detail', args=[self.project.id]) + 'invite/'
        data = {'invitations_list': [
            {'id': self.user_to_operations.id},
        ]}
        self.client.force_authenticate(user=self.user_not_owner)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_proj_get_invitations(self):
        inv = ProjectInvitation.objects.create(owner=self.user_to_operations, project=self.project_to_update)
        url = reverse('projects:project-detail', args=[self.project_to_update.id]) + 'get_invitations/'
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('id' in resp.data[0])
        self.assertTrue('owner' in resp.data[0])
        self.assertTrue('is_accepted' in resp.data[0])

    def test_remove_participants(self):
        url = reverse('projects:project-detail', args=[self.project.id]) + 'remove_participants/'
        self.project.add_participant(self.user_to_operations)
        data = {
            'to_remove_list' :[
                {'id': self.user_to_operations.id}
            ]
        }
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.post(url,data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_to_operations not in self.project.participants.all())

    def test_remove_participants_fail_auth_unauthorized(self):
        url = reverse('projects:project-detail', args=[self.project.id]) + 'remove_participants/'
        self.client.force_authenticate(user=self.user_not_owner)
        data = {
            'to_remove_list': [
                {'id': self.user_to_operations.id}
            ]
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_participants_404(self):
        url = reverse('projects:project-detail', args=[100000]) + 'remove_participants/'
        self.client.force_authenticate(user=self.user_owner)
        data = {
            'to_remove_list': [
                {'id': self.user_to_operations.id}
            ]
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
'''
    Code needs refactor , less code replications
'''

class InvitationViewSetTest(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create(email='test_email@gmail.com',
                                                  first_name='aDam',
                                                  last_name='Smith',
                                                  password='!*&!*(HN'
                                                  )
        self.user_to_operations = User.objects.create(email='2test_email@gmail.com',
                                                           first_name='aDam',
                                                           last_name='Smith',
                                                           password='!*&!*(HN'
                                                           )
        self.user_not_authorized = User.objects.create(email='3test_email@gmail.com',
                                                           first_name='aDam',
                                                           last_name='Smith',
                                                           password='!*&!*(HN'
                                                           )

        self.project = Project.objects.create(
            project_name= 'test',
            owner= self.user_owner
        )
        self.project2 = Project.objects.create(
            project_name='test',
            owner=self.user_owner
        )
        self.invitation = ProjectInvitation.objects.create(
            owner = self.user_to_operations,
            project = self.project
        )
        self.invitation2 = ProjectInvitation.objects.create(
            owner=self.user_to_operations,
            project=self.project2
        )

    def test_list(self):
        url= reverse('projects:invitations-list')
        self.client.force_authenticate(user=self.user_to_operations)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('owner' in resp.data[0])
        self.assertTrue('project' in resp.data[0])
        self.assertTrue('is_accepted' in resp.data[0])
        self.assertTrue('id' in resp.data[0])

    def test_destroy_invited(self):
        url = reverse('projects:invitations-detail', args=[self.invitation.id])
        self.client.force_authenticate(user=self.user_to_operations)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(ProjectInvitation.objects.filter(pk=self.invitation.id).exists())


    def test_destroy_inviting(self):
        url = reverse('projects:invitations-detail', args=[self.invitation.id])
        self.client.force_authenticate(user=self.user_owner)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertFalse(ProjectInvitation.objects.filter(pk=self.invitation.id).exists())

    def test_destroy_unauthorized(self):
        url = reverse('projects:invitations-detail', args=[self.invitation.id])
        self.client.force_authenticate(user=self.user_not_authorized)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(ProjectInvitation.objects.filter(pk=self.invitation.id).exists())

    def test_destroy_404(self):
        url = reverse('projects:invitations-detail', args=[100000])
        self.client.force_authenticate(user=self.user_to_operations)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_accept(self):
        self.assertFalse(self.user_to_operations in self.project.participants.all())
        url = reverse('projects:invitations-detail', args=[self.invitation.id]) + 'accept/'
        self.client.force_authenticate(user=self.user_to_operations)
        resp = self.client.get(url)
        updated_inv = ProjectInvitation.objects.get(pk = self.invitation.id)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_to_operations in self.project.participants.all())
        self.assertEqual(updated_inv.is_accepted, True)

    def test_accept_404(self):
        url = reverse('projects:invitations-detail', args=[100000]) + 'accept/'
        self.client.force_authenticate(user=self.user_to_operations)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_accept_unauthorized(self):
        url = reverse('projects:invitations-detail', args=[self.invitation.id]) + 'accept/'
        self.client.force_authenticate(user=self.user_not_authorized)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


































