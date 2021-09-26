# Generated by Django 3.2.4 on 2021-09-04 03:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_memberrecordsimport_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberrecordsimport',
            name='report_date',
            field=models.DateField(default=django.utils.timezone.now, unique=True, verbose_name='Date the report was generated'),
            preserve_default=False,
        ),
    ]