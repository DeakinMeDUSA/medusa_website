# Generated by Django 3.2.10 on 2022-01-21 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20220121_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationtype',
            name='machine_type',
            field=models.CharField(help_text='Machine readable type, autogenerated from type', max_length=256, null=True),
        ),
    ]
