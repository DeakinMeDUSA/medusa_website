# Generated by Django 3.1.3 on 2020-12-07 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_bank', '0006_auto_20201207_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(blank=None, choices=[('CARDIOLOGY', 'Cardiology'), ('NEUROLOGY', 'Neurology'), ('PAEDIATRICS', 'Paediatrics')], default=None, max_length=128, null=True),
        ),
    ]