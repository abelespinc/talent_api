from __future__ import annotations

from rest_framework import serializers

from talent.core.models import Configuration
from talent.users.models import User


class ModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Manually add the "created_by" field to every serializer
        if "created_by" not in self.fields:
            self.fields["created_by"] = serializers.PrimaryKeyRelatedField(
                queryset=User.objects.all(),
                write_only=True,
                required=False,
                allow_null=True,
            )


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        return self.get_queryset().get_or_create(**{self.slug_field: data})[0]


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = [
            "status_scrapy_enabled",
            "status_scrapy_periodicity",
            "status_scrapy_days_to_start",
            "status_scrapy_duration",
            "scrapy_job_keywords",
        ]


class ConfigurationScrapySerializer(ConfigurationSerializer):
    class Meta(ConfigurationSerializer.Meta):
        fields = [
            "status_scrapy_enabled",
            "status_scrapy_periodicity",
            "status_scrapy_days_to_start",
            "status_scrapy_duration",
            "scrapy_job_keywords",
        ]
