# Generated by Django 5.0.4 on 2024-04-15 11:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_alter_appointment_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointmentTime',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
