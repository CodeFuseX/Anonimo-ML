# Generated by Django 3.2.4 on 2022-04-01 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0005_rename_report_reportdoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportdoc',
            name='completed_reports',
            field=models.IntegerField(default=0, max_length=1000),
        ),
    ]