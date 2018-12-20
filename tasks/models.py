from django.db import models
import time



class TaskManager(models.Manager):
    use_in_migrations = True

    def create_main_task(self, **validated_data):
        task = self.model(**validated_data)
        task.save(using=self._db)
        return task

    def create(self, **validated_data):
        task = self.model(**validated_data)
        project = Task.objects.get(parent_task=validated_data['parent_task'])
        task.save(using=self._db)

class Task(models.Model):
    objects = TaskManager()

    project = models.OneToOneField(
        'permissions.Project',
        related_name='projectTasks',
        on_delete=models.CASCADE
    )
    is_main = models.BooleanField(default=False)
    name = models.TextField(max_length=120, blank=False)
    description = models.TextField(max_length=120, blank=True)
    parent_task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

