# Generated by Django 3.2.4 on 2021-07-21 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_supporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supporter',
            name='image',
            field=models.ImageField(help_text='Supporter image for display on frontend', null=True, upload_to='frontend/sponsors'),
        ),
    ]
