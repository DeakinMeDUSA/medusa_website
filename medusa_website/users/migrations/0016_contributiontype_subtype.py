# Generated by Django 3.2.10 on 2022-01-03 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_contributioncertificate_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributiontype',
            name='subtype',
            field=models.CharField(choices=[('WEBSITE', 'WEBSITE'), ('EVENTS', 'EVENTS'), ('OTHER', 'OTHER')], default='OTHER', max_length=128),
        ),
    ]
