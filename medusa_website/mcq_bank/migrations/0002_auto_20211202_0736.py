# Generated by Django 3.2.9 on 2021-12-01 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mcq_bank', '0001_inital'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Quiz',
        ),
        migrations.AlterModelOptions(
            name='quizsession',
            options={},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer_order',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='mcq_bank.question', verbose_name='Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='users.user', verbose_name='User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='answer_image',
            field=models.ImageField(blank=True, help_text='Upload an image to be shown with the answers', null=True, upload_to='', verbose_name='Answer Image'),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='questions', to='mcq_bank.category', verbose_name='Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='flagged_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='flagged_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='flagged_message',
            field=models.TextField(blank=True, help_text='Explanation for why the question was flagged.', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='is_flagged',
            field=models.BooleanField(default=False, help_text='If True, has been flagged by a user'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_reviewed',
            field=models.BooleanField(default=False, help_text='If True, has been reviewed by a staff or admin'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_image',
            field=models.ImageField(blank=True, help_text='Upload an image to be shown in the question prompt', null=True, upload_to='', verbose_name='Question Image'),
        ),
        migrations.AddField(
            model_name='question',
            name='randomise_answer_order',
            field=models.BooleanField(default=True, help_text='If True (default), answers will be displayed in a random order each time', verbose_name='Randomise answer order?'),
        ),
        migrations.AddField(
            model_name='question',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reviewed_questions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quizsession',
            name='answers',
            field=models.ManyToManyField(blank=True, related_name='quiz_sessions', to='mcq_bank.Answer'),
        ),
        migrations.AddField(
            model_name='quizsession',
            name='current_question_index',
            field=models.IntegerField(default=0, verbose_name='Index of the question currently being answered'),
        ),
        migrations.AddField(
            model_name='quizsession',
            name='questions',
            field=models.ManyToManyField(blank=True, related_name='quiz_sessions', to='mcq_bank.Question'),
        ),
        migrations.AddField(
            model_name='quizsession',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='quiz_sessions', to='users.user', verbose_name='User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='explanation',
            field=models.TextField(blank=True, help_text='Extra explanation for this answer', null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(help_text='Enter the answer text that you want displayed', verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=martor.models.MartorField(blank=True, help_text='Explanation to be shown after the question has been answered', null=True, verbose_name='Explanation'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(help_text='Enter the question text that you want displayed', unique=True, verbose_name='Question text'),
        ),
        migrations.AlterField(
            model_name='record',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='mcq_bank.answer'),
        ),
        migrations.AlterField(
            model_name='record',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='mcq_bank.question'),
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]
