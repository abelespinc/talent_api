# Generated by Django 4.1.1 on 2022-10-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("offers", "0008_offer_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="status",
            field=models.TextField(
                blank=True,
                choices=[
                    (None, "(Null)"),
                    ("ACTIVE", "Active"),
                    ("NOT_ACTIVE", "Not active"),
                    ("NO_STATUS", "No status"),
                    ("HTTP_ERROR", "HTTP Error"),
                    ("XPATH_ERROR", "XPATH Error"),
                ],
                default="ACTIVE",
                verbose_name="Status",
            ),
        ),
    ]
