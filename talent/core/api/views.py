from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from talent.core.api.serializers import ConfigurationScrapySerializer
from talent.core.api.serializers import ConfigurationSerializer
from talent.core.models import Configuration


class ModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """
        Only work with active objects by default
        """

        if hasattr(self.queryset.model, "is_active"):
            # Not all models have the is_active field and we avoid the error "AttributeError: 'ModelViewSet' object
            # has no attribute 'is_active'"
            return super().get_queryset().filter(is_active=True)

        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.pk  # Set the "created_by" field to the user that made the request
        return super().create(request, *args, **kwargs)


class ConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = ConfigurationSerializer
    queryset = Configuration.objects.all()

    def get_object(self):
        return self.get_queryset().first()

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=False, serializer_class=ConfigurationScrapySerializer)
    def scrapy(self, request):
        return self.retrieve(request)

    @scrapy.mapping.patch
    def patch_scrapy(self, request):
        return self.partial_update(request)
