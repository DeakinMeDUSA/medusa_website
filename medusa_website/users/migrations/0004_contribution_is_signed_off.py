# Generated by Django 3.2.10 on 2022-01-01 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220101_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='is_signed_off',
            field=models.BooleanField(default=False),
        ),
    ]