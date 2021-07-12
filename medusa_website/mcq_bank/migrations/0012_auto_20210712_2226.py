# Generated by Django 3.2.4 on 2021-07-12 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mcq_bank', '0011_auto_20210712_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='mcq_bank.question', verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='mcq_bank.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='question',
            name='flagged_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flagged_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reviewed_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quizsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quiz_sessions', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
