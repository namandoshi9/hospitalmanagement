# Generated by Django 5.0.4 on 2024-04-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0029_alter_appointment_app_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='app_mode',
            field=models.CharField(choices=[('Offline', 'Offline'), ('Online', 'Online')], default='offline', max_length=10),
        ),
    ]
