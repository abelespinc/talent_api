import json

from django.db.models import Q
from django.http import Http404

from cities_light.models import City
from cities_light.models import SubRegion
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from talent.core.api.views import ModelViewSet
from talent.jobs.utils import LocationTypes
from talent.offers.api.serializers import OfferAiInfoSerializer
from talent.offers.api.serializers import OfferDetailReadSerializer
from talent.offers.api.serializers import OfferDuplicateSerializer
from talent.offers.api.serializers import OfferReadSerializer
from talent.offers.api.serializers import OfferWriteSerializer
from talent.offers.api.serializers import RecruiterSerializer
from talent.offers.api.serializers import SourceSerializer
from talent.offers.models import Offer
from talent.offers.models import OfferAiInfo
from talent.offers.models import OfferDuplicate
from talent.offers.models import Recruiter
from talent.offers.models import Source
from talent.offers.services.offers import get_filtered_offers


class OfferViewSet(ModelViewSet):
    serializer_class = OfferReadSerializer
    queryset = Offer.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, offer_id=self.kwargs[self.lookup_field])

            # May raise a permission denied
            self.check_object_permissions(self.request, obj)

            return obj

    def get_serializer_class(self):
        detail = json.loads(self.request.query_params.get("detail", "false"))

        if self.action == "retrieve" or (self.action == "list" and detail):
            return OfferDetailReadSerializer

        if self.action in ["create", "update", "partial_update"]:
            return OfferWriteSerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return get_filtered_offers(params=self.request.query_params, initial_qs=super().get_queryset())

    @action(detail=True)
    def duplicates(self, request, pk):
        offer = self.get_object()
        duplicate_offers = OfferDuplicate.objects.filter(Q(from_offer=offer) | Q(to_offer=offer))

        serializer = OfferDuplicateSerializer(instance=duplicate_offers, many=True)

        return Response(serializer.data)

    @duplicates.mapping.delete
    def delete_duplicates(self, request, pk):
        offer = self.get_object()
        duplicate_offers = OfferDuplicate.objects.filter(Q(from_offer=offer) | Q(to_offer=offer))
        duplicate_offers.delete()

        return Response()

    @action(methods=["PATCH"], detail=True, url_path="standard-location")
    def standard_location(self, request, pk):
        location_data = request.data["location"]
        offer = self.get_object()

        if location := offer.location:
            if location_data["type"] == LocationTypes.SUBREGION:
                location.subregion = SubRegion.objects.get(pk=location_data["id"])
            elif location_data["type"] == LocationTypes.CITY:
                location.city = City.objects.get(pk=location_data["id"])
            else:
                raise ValidationError("Invalid location type")

            location.save()

        return Response()


class SourceViewSet(ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()


class RecruiterViewSet(ModelViewSet):
    serializer_class = RecruiterSerializer
    queryset = Recruiter.objects.all()


class OfferDuplicateViewSet(ModelViewSet):
    serializer_class = OfferDuplicateSerializer
    queryset = OfferDuplicate.objects.all()


class OfferAiInfoViewSet(ModelViewSet):
    serializer_class = OfferAiInfoSerializer
    queryset = OfferAiInfo.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        offer = self.request.query_params.get("offer")

        if offer:
            queryset = queryset.filter(offer=offer)

        return queryset
