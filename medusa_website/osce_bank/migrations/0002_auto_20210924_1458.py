# Generated by Django 3.2.4 on 2021-09-24 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('osce_bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'ordering': ('level',)},
        ),
        migrations.AlterModelOptions(
            name='speciality',
            options={'ordering': ('speciality',), 'verbose_name': 'Speciality', 'verbose_name_plural': 'Specialities'},
        ),
        migrations.AlterModelOptions(
            name='stationtype',
            options={'ordering': ('station_type',)},
        ),
        migrations.AlterField(
            model_name='oscestation',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stations', to='osce_bank.level'),
        ),
    ]
