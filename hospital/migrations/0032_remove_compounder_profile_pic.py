# Generated by Django 3.0.5 on 2024-04-09 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0031_auto_20240409_1559'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compounder',
            name='profile_pic',
        ),
    ]
