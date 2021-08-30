# Generated by Django 3.2.4 on 2021-08-29 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_bank', '0017_auto_20210713_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quizsession',
            options={},
        ),
        migrations.AddField(
            model_name='quizsession',
            name='current_question_index',
            field=models.IntegerField(default=0, verbose_name='Index of the question currently being answered'),
        ),
    ]
