from django.db import models

class TaskPermission(models.Model):
    PERMISSION_TYPE_CHOICES = (
        ("READ", "Read"),  # Read only the task and subtasks,
        ("EDIT", "Edit")  # Full task and subtasks permissions
    )

    owner = models.ForeignKey(
        'UserManagement.User',
        on_delete=models.CASCADE
    )

    target = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='taskPermission'
    )
    permission_type = models.CharField(
        max_length=4,
        choices=PERMISSION_TYPE_CHOICES,
        default="READ"
    )

class TaskManager(models.Manager):
    use_in_migrations = True

    def create(self, parent, **validated_data):
        task = self.model(**validated_data)
        task.parent_task = parent
        task.save(using=self._db)
        return task


class Task(models.Model):
    objects = TaskManager()

    project = models.ForeignKey(
        'projects.Project',
        related_name='assignedTasks',
        on_delete=models.CASCADE
    )
    name = models.TextField(max_length=120, blank=False)
    description = models.TextField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def push_sub_task(self, **validated_data):
        validated_data['project'] = self.project
        new_task = Task.objects.create(self, **validated_data)
        return new_task

    def chceck_permission(self, user):
        return TaskPermission.objects.filter(target=self, owner=user).exists()

    def get_sub_tasks(self):
        return Task.objects.sub_tasks


class TaskPart(models.Model):
    partent = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,

    )
    name = models.TextField(max_length=1000)
    description = models.TextField(max_length=10000)


# class GroupTaskPermission(models.Model):
#     group = models.ForeignKey(
#         'UserManagement.Group',
#         on_delete=models.CASCADE
#     )
#     target = models.ForeignKey('Task', on_delete=models.CASCADE)


