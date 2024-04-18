# Generated by Django 5.0.4 on 2024-04-17 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0010_remove_prescription_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointmentTime',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
