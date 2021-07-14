# Generated by Django 3.2.4 on 2021-07-09 09:36

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_bank', '0008_alter_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=martor.models.MartorField(help_text='Explanation to be shown after the question has been answered', max_length=2000, verbose_name='Explanation'),
        ),
    ]