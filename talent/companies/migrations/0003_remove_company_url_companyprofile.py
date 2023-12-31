# Generated by Django 4.1.1 on 2022-10-13 10:08

import uuid

import django.core.serializers.json
import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("offers", "0004_remove_offer_title_offer_job"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("companies", "0002_alter_company_name_alter_industry_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="url",
        ),
        migrations.CreateModel(
            name="CompanyProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(blank=True, default=True, verbose_name="Is active?"),
                ),
                (
                    "extra_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=django.core.serializers.json.DjangoJSONEncoder,
                        verbose_name="Extra data",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Creation date"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Last modification date"),
                ),
                ("url", models.URLField(blank=True, null=True, verbose_name="URL")),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profiles",
                        to="companies.company",
                        verbose_name="Company",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="company_profiles",
                        to="offers.source",
                        verbose_name="Source",
                    ),
                ),
            ],
            options={
                "verbose_name": "Company profile",
                "verbose_name_plural": "Company profiles",
            },
        ),
    ]
