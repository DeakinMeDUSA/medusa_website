# Generated by Django 3.1.6 on 2021-04-04 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mcq_bank', '0003_quizsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizsession',
            name='answers',
            field=models.ManyToManyField(blank=True, null=True, related_name='quiz_sessions', to='mcq_bank.Answer'),
        ),
        migrations.AlterField(
            model_name='quizsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_sessions', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
