# Generated by Django 5.0.4 on 2024-04-17 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0011_alter_appointment_appointmentdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='admitDate',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]