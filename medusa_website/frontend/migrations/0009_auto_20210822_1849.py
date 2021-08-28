# Generated by Django 3.2.4 on 2021-08-22 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0008_conferencereport'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectiveReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elective_name', models.CharField(help_text='Name of the elective', max_length=256)),
                ('elective_year', models.IntegerField(help_text='Year of the elective, e.g 2018')),
                ('elective_city', models.CharField(help_text="City where the elective took place, e.g. 'Canberra'", max_length=128)),
                ('report_author', models.CharField(help_text='Name of the author of the report', max_length=256)),
                ('file', models.FileField(upload_to='tcss_reports')),
            ],
        ),
        migrations.AlterField(
            model_name='conferencereport',
            name='conference_year',
            field=models.IntegerField(help_text='Year of the conference, e.g 2018'),
        ),
    ]