# Generated by Django 5.0.4 on 2024-04-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0019_appointment_a_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='barcode_value',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
