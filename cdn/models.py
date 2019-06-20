from django.db import models
from datetime import datetime
import os
from . import config
from django.conf import settings


class ImageManager(models.Manager):

    def create(self, owner, **validated_data):
        img = self.model()
        img.owner = owner
        img.set_image(validated_data['profile_image'])
        img.save(using=self._db)
        return img


class ProfileImage(models.Model):
    objects = ImageManager()

    owner = models.OneToOneField(
        'UserManagement.User',
        on_delete=models.CASCADE,
        related_name='profileImage'
    )
    image = models.ImageField(upload_to=f'{settings.CDN_ROOT_RELATIVE}/{config.PROFILE_IMAGES_PATH}')
    url = models.TextField(max_length=5000)
    name = models.TextField(max_length=5000)

    def set_name(self, img):
        if not self.owner:
            print("First you need to set image owner")
            raise AttributeError
        filename, extenstion = os.path.splitext(img.name)
        self.name = f'{self.owner.id}_profile_pic{extenstion}'
        img.name = self.name
        return img

    def set_image(self, img):
        img = self.set_name(img)
        self.image = img
        self.set_url()

    def set_url(self):
        self.url = f'{config.PROFILE_IMAGES_PATH}/{self.name}'

    def update(self, **validated_data):
        self.set_image(validated_data["profile_image"])
        self.save()
        return self

    def get_absolute_url(self):
        return settings.CDN_URL + self.url



class SubTaskFileManager(models.Manager):

    def create(self, sub_task, **validated_data):
        img = self.model()
        img.sub_task = sub_task
        img.set_image(validated_data['profile_image'])
        img.save(using=self._db)
        return img


class TaskFile(models.Model):
    objects = SubTaskFileManager()

    sub_task = models.ForeignKey(
        'tasks.SubTask',
        on_delete=models.CASCADE,
        related_name='subTaskFiles'
    )
    owner = models.OneToOneField(
        'UserManagement.User',
        on_delete=models.CASCADE,
        related_name='uploadedSubTaskFiles'
    )
    file = models.FileField(upload_to=f'{settings.CDN_ROOT_RELATIVE}/{config.TASK_IMAGES_PATH}')
    url = models.TextField(max_length=5000)
    name = models.TextField(max_length=5000)

    def set_name(self, img):
        if not self.sub_task:
            print("First you need to set image owner")
            raise AttributeError
        filename, extenstion = os.path.splitext(img.name)
        self.name = f'{self.id}_file_{extenstion}'
        img.name = self.name
        return img

    def set_image(self, img):
        img = self.set_name(img)
        self.image = img
        self.set_url()

    def set_url(self):
        self.url = f'{config.TASK_IMAGES_PATH}/{self.name}'

    def update(self, **validated_data):
        self.set_image(validated_data["profile_image"])
        self.save()
        return self

    def get_absolute_url(self):
        return settings.CDN_URL + self.url




