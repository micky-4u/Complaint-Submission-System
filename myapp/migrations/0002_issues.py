# Generated by Django 4.2.4 on 2023-08-22 18:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('issue_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=200)),
                ('room_number', models.PositiveIntegerField(default=0)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('solved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
