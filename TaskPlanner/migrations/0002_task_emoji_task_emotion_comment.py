# Generated by Django 5.0 on 2024-01-11 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskPlanner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='emoji',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='emotion_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
