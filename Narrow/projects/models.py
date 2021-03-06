from django.db import models
from django.db.models import Q
from tasks.models import Task


class ProjectManager(models.Manager):
    use_in_migrations = True

    def create(self, **validated_data):
        project = self.model(**validated_data)
        project.save(using=self._db)
        # Auto adds owner as participant of project
        project.participants.add(project.owner)
        return project


class Project(models.Model):
    objects = ProjectManager()

    owner = models.ForeignKey(
        'UserManagement.User',
        on_delete=models.CASCADE,
    )
    project_name = models.TextField(max_length=100, blank=False)
    description = models.TextField(max_length=1000, blank=True)
    participants = models.ManyToManyField(
        "UserManagement.User",
        blank=True,
        related_name='projectList'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_participant(self, user):
        self.participants.add(user)

    def remove_participants(self, participants_list):
        for participant in participants_list:
            self.participants.remove(participant)

    def update(self, **validated_data):
        for attr, value in validated_data.items():
            setattr(self, attr, value)
        self.save()
        return self


# class Group(models.Model):
#     project = models.ForeignKey(
#         'Project',
#         on_delete=models.CASCADE,
#     )
#     name = models.TextField(max_length=100, blank=False)
#     participants = models.ManyToManyField(
#         "UserManagement.User",
#         blank=True,
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class ProjectInvitation(models.Model):
    owner = models.ForeignKey(
        'UserManagement.User',
        on_delete=models.CASCADE,
        related_name='invited_to',
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='invited_users'
    )
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def delete_with_duplicates(self):
        invitations = ProjectInvitation.objects.filter(
            Q(owner=self.owner) & Q(project=self.project)
        )
        invitations.delete()

    def accept(self):
        self.project.add_participant(self.owner)
        self.is_accepted = True
        self.save()
        return self

    def reject(self):
        self.is_rejected = True
        self.save()
        return self


