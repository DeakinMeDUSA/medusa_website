# Generated by Django 3.2.10 on 2021-12-26 06:57

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    replaces = [('org_chart', '0001_initial'), ('org_chart', '0002_alter_subcommitee_org_chart_fill_color'), ('org_chart', '0003_auto_20210719_2155'), ('org_chart', '0004_auto_20210719_2200'), ('org_chart', '0005_subcommittee_explanation_text'), ('org_chart', '0006_alter_committeemember_profile_pic')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubCommittee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('org_chart_fill_color', colorfield.fields.ColorField(default='#000000', help_text='Should be a CSS compatible hex colour', image_field=None, max_length=18, samples=None)),
                ('explanation_text', tinymce.models.HTMLField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the current holder of the position', max_length=128)),
                ('position', models.CharField(help_text='Name of the position', max_length=128, unique=True)),
                ('email', models.EmailField(help_text='Must be a medusa.org.au email, not the personal email of the position holder', max_length=254)),
                ('profile_pic', models.ImageField(blank=True, help_text='Profile pic of the current committee member', null=True, upload_to='org_chart/images')),
                ('sub_committee', models.ForeignKey(help_text='Subcommittee the position belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='members', to='org_chart.subcommittee')),
            ],
        ),
    ]
