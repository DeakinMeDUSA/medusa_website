# Generated by Django 3.2.10 on 2022-01-03 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org_chart', '0005_committeememberrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='committeerole',
            name='email',
            field=models.EmailField(help_text='Must not be the personal email of the position holder', max_length=254, unique=True),
        ),
    ]
