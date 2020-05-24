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

    def create(self, **validated_data):
        task = self.model(**validated_data)
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
        return self.sub_tasks


class SubTask(models.Model):
    parent = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='sub_tasks'

    )
    name = models.TextField(max_length=1000)
    description = models.TextField(max_length=10000)
    is_completed = models.BooleanField(default=False)
    deadline = models.TimeField(null=True, blank=True)

    def complete(self):
        self.is_completed = True
        self.save()
        return self

# class SubTaskAssignment(models.Manager):
#     use_in_migrations = True
#
#     def create(self, **validated_data):
#         assignment = self.model(**validated_data)
#         assignment.save(using=self._db)
#         # return task

class SubTaskAssignment(models.Model):
    user = models.ForeignKey(
        'UserManagement.User',
        on_delete=models.CASCADE
    )
    sub_task = models.ForeignKey(
        'SubTask',
        on_delete=models.CASCADE,
    )


# class GroupTaskPermission(models.Model):
#     group = models.ForeignKey(
#         'UserManagement.Group',
#         on_delete=models.CASCADE
#     )
#     target = models.ForeignKey('Task', on_delete=models.CASCADE)


