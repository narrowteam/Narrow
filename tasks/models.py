from django.db import models



class TaskManager(models.Manager):
    use_in_migrations = True

    def create_main_task(self, **validated_data):
        task = self.model(**validated_data)
        task.is_main = True
        task.save(using=self._db)
        return task

    def create(self, parent, **validated_data):
        task = self.model(**validated_data)
        task.parent_task = parent
        task.project = Task.objects.get(pk=parent.pk).project
        task.save(using=self._db)
        return task


class Task(models.Model):
    objects = TaskManager()

    project = models.ForeignKey(
        'permissions.Project',
        related_name='main_task',
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

    def push_sub_task(self, **validated_data):
        new_task = Task.objects.create(self, **validated_data)
        return new_task


