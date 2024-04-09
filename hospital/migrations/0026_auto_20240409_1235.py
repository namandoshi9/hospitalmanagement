# Generated by Django 3.0.5 on 2024-04-09 07:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0025_compounder_first_name_compounder_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='doctorId',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='doctorName',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patientId',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patientName',
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.Doctor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.Patient'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(),
        ),
    ]