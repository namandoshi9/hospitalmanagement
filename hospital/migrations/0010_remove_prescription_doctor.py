# Generated by Django 5.0.4 on 2024-04-17 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_remove_prescription_p_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='doctor',
        ),
    ]
