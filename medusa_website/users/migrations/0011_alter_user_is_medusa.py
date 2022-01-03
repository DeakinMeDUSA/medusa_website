# Generated by Django 3.2.10 on 2022-01-03 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20220103_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_medusa',
            field=models.BooleanField(default=False, help_text='Designates whether this user has medusa.org.au email address.', verbose_name='Is a medusa.org.au user'),
        ),
    ]
