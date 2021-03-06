from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q

class UserSettings(models.Model):
    owner = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name='settings'
    )
    email_notifications_on_events = models.BooleanField(
        default=True,
    )
    is_email_public = models.BooleanField(
        default=False,
    )


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def search(self, **kwargs):
        return

    def matching_full_name(self, request,  full_name):
        keywords = full_name.split(' ')
        if len(keywords) == 1:
            keywords.append('')
        return self.exclude(id=request.user.id).filter(
            Q(first_name__contains=keywords[0], last_name__contains=keywords[1])
            |
            Q(last_name__contains=keywords[0], first_name__contains=keywords[1])
        )[:20]

    # for manage.py
    def create_superuser(self, email, password):
        user = self.model(
            email=email,
            is_staff=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create(self, **validated_data):
        if validated_data['first_name']:
            validated_data['first_name'] = validated_data['first_name'].capitalize()
        if validated_data['last_name']:
            validated_data['last_name'] = validated_data['last_name'].capitalize()

        user = self.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save(using=self._db)
        UserSettings.objects.create(owner=user)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, blank=True)
    email = models.EmailField(
        max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(
        max_length=127, unique=False, blank=False, null=False)
    last_name = models.CharField(
        max_length=127, unique=False, blank=False, null=False)
    registration_datetime = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['email',]

    class Meta:
        db_table = "users"
        app_label = 'UserManagement'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    def update_user(self, **validated_data):
        if 'first_name' in validated_data:
            validated_data['first_name'] = validated_data['first_name'].capitalize()
        if 'last_name' in validated_data:
            validated_data['last_name'] = validated_data['last_name'].capitalize()

        for attr, value in validated_data.items():
            setattr(self, attr, value)
        self.save()




