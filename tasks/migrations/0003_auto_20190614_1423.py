# Generated by Django 2.2.2 on 2019-06-14 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190611_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_main',
        ),
        migrations.RemoveField(
            model_name='task',
            name='parent_task',
        ),
        migrations.AlterField(
            model_name='taskpermission',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskPermission', to='tasks.Task'),
        ),
        migrations.CreateModel(
            name='TaskPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=1000)),
                ('description', models.TextField(max_length=10000)),
                ('partent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
        ),
    ]
