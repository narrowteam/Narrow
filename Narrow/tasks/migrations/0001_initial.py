# Generated by Django 2.1.3 on 2018-12-22 12:54

from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField(default=False)),
                ('name', models.TextField(max_length=120)),
                ('description', models.TextField(blank=True, max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_task', to='projects.Project')),
            ],
            managers=[
                ('objects', tasks.models.TaskManager()),
            ],
        ),
    ]
