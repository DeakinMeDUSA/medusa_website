# Generated by Django 3.2.10 on 2022-01-02 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_contributioncertificate_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
    ]
