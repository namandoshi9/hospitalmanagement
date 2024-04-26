# Generated by Django 5.0.4 on 2024-04-25 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0026_appointment_staff_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='app_mode',
            field=models.CharField(choices=[('', '-------- Appointment Mode --------'), ('Online', 'Online'), ('Offline', 'Offline')], default='offline', max_length=10),
        ),
    ]
