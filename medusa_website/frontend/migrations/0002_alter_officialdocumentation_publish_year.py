# Generated by Django 3.2.10 on 2021-12-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_squashed_0010_auto_20210822_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officialdocumentation',
            name='publish_year',
            field=models.IntegerField(),
        ),
    ]