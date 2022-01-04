# Generated by Django 3.2.10 on 2022-01-04 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20220104_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributioncertificate',
            name='date_sent_for_signoff',
            field=models.DateField(blank=True, help_text='Date the certificate was requested for signoff', null=True),
        ),
        migrations.AddField(
            model_name='contributioncertificate',
            name='sent_for_signoff',
            field=models.BooleanField(default=False, help_text='True if sent for signoff'),
        ),
    ]
