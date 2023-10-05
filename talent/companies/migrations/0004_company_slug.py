# Generated by Django 4.1.1 on 2022-10-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0003_remove_company_url_companyprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=256, verbose_name="Name slug"
            ),
        ),
    ]
