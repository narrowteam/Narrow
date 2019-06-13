from django.db import models
from datetime import datetime
import os


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
    image = models.ImageField(upload_to='cdn_data/pictures/profile_pictures')
    url = models.TextField(max_length=5000)
    name = models.TextField(max_length=5000)

    def set_name(self, img):
        if not self.owner:
            print("First you need to set image owner")
            raise AttributeError
        filename, extenstion = os.path.splitext(img.name)
        self.name = f'{self.owner.id}_{datetime.now()}_profile_pic{extenstion}'
        img.name = self.name
        return img

    def set_image(self, img):
        img = self.set_name(img)
        self.image = img
        self.set_url()

    def set_url(self):
        self.url = f'/cdn/{self.name}'
        return self


    def update(self, **validated_data):
        self.set_image(validated_data["profile_image"])
        self.save()
        return self



