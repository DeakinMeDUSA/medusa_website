# Generated by Django 3.2.4 on 2021-06-28 06:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mcq_bank', '0006_auto_20210614_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer_order',
        ),
        migrations.AddField(
            model_name='question',
            name='randomise_answer_order',
            field=models.BooleanField(default=True, help_text='If True (default), answers will be displayed in a random order each time', verbose_name='Randomise answer order?'),
        ),
        migrations.AlterField(
            model_name='history',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(help_text='Explanation to be shown after the question has been answered', max_length=2000, verbose_name='Explanation'),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload an image supporting the question', null=True, upload_to='', verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='record',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to='mcq_bank.answer'),
        ),
        migrations.AlterField(
            model_name='record',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
    ]