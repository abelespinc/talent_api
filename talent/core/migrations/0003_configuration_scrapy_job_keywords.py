# Generated by Django 4.1.1 on 2022-11-23 11:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_configuration_status_scrapy_enabled"),
    ]

    operations = [
        migrations.AddField(
            model_name="configuration",
            name="scrapy_job_keywords",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(), blank=True, default=list, size=None
            ),
        ),
    ]