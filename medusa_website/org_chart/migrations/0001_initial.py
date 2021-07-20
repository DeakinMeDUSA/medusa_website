# Generated by Django 3.2.4 on 2021-07-19 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubCommitee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('org_chart_fill_color', models.CharField(help_text='Should be a CSS compatible hex, rgb, etc colour', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CommiteeMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the current holder of the position', max_length=128)),
                ('position', models.CharField(help_text='Name of the position', max_length=128)),
                ('email', models.EmailField(help_text='Must be a medusa.org.au email, not the personal email of the position holder', max_length=254)),
                ('profile_pic', models.ImageField(help_text='Profile pic of the current commitee member', upload_to='org_chart/images')),
                ('sub_committe', models.ForeignKey(help_text='Subcommitee the position belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='members', to='org_chart.subcommitee')),
            ],
        ),
    ]
