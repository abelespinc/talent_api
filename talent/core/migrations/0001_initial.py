# Generated by Django 4.1.1 on 2022-10-27 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status_scrapy_periodicity",
                    models.SmallIntegerField(
                        blank=True,
                        default=2,
                        help_text="Active offers will be checked every X days",
                        verbose_name="Status scrapy periodicity",
                    ),
                ),
                (
                    "status_scrapy_days_to_start",
                    models.SmallIntegerField(
                        blank=True,
                        default=4,
                        help_text="Active offers will be checked X days after they are saved",
                        verbose_name="Status scrapy days to start",
                    ),
                ),
                (
                    "status_scrapy_duration",
                    models.SmallIntegerField(
                        blank=True,
                        default=14,
                        help_text="Active offers will be checked for X days",
                        verbose_name="Status scrapy duration",
                    ),
                ),
            ],
            options={
                "verbose_name": "Configuration",
                "verbose_name_plural": "Configuration",
            },
        ),
    ]
