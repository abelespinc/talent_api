# Generated by Django 4.1.1 on 2022-11-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="configuration",
            name="status_scrapy_enabled",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="Is the scrapy enabled?",
                verbose_name="Status scrapy enabled",
            ),
        ),
    ]
