# Generated by Django 3.2.10 on 2022-01-04 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_contributioncertificate_is_signed_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributioncertificate',
            name='preview_pdf',
            field=models.FileField(blank=True, null=True, upload_to='contribution_certificates/previews'),
        ),
        migrations.AddField(
            model_name='contributioncertificate',
            name='signed_pdf',
            field=models.FileField(blank=True, null=True, upload_to='contribution_certificates/signed'),
        ),
    ]
