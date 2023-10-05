from __future__ import annotations

from typing import TYPE_CHECKING
from typing import TypedDict

from django.contrib.postgres.lookups import Unaccent
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.db.models import Value
from django.db.models.functions import Lower

from cities_light.models import City
from cities_light.models import SubRegion

from talent.jobs.utils import LocationTypes

if TYPE_CHECKING:
    from talent.jobs.models import Location


class LocationForSearch(TypedDict):
    id: int
    name: str
    type: LocationTypes


def get_location_model_from_location_type(*, location_type: LocationTypes):
    if location_type == LocationTypes.SUBREGION:
        return SubRegion
    if location_type == LocationTypes.CITY:
        return City
    raise ValueError(f"Invalid location type {location_type}")


def get_standard_locations_from_location_name(
    *,
    location_name: str,
    location_type: LocationTypes,
    for_search=False,
) -> QuerySet:
    """
    Return a standard django-cities object from the given city name.
    Since the city name can be anything, we need to use PostgreSQL search techniques to find the best match.
    """
    # Normalize city name to lower case and remove accents
    normalized_city_name = Lower(Unaccent(Value(location_name)))

    Location = get_location_model_from_location_type(location_type=location_type)
    trigram_similarity = TrigramSimilarity(Lower(Unaccent("name")), normalized_city_name)
    similarity_threshold = 0.2 if for_search else 0.5

    return (
        Location.objects.annotate(similarity=trigram_similarity)
        .filter(similarity__gt=similarity_threshold)
        .order_by("-similarity")
    )


def get_standard_location_from_location_name(*, location_name: str, location_type: LocationTypes):
    locations = get_standard_locations_from_location_name(location_name=location_name, location_type=location_type)

    # Return the most relevant result if one exists, otherwise None
    return locations.first() if locations.exists() else None


def get_standard_subregion_from_subregion_name(*, subregion_name: str):
    return get_standard_location_from_location_name(location_name=subregion_name, location_type="SUBREGION")


def get_standard_city_from_city_name(*, city_name: str):
    return get_standard_location_from_location_name(location_name=city_name, location_type="CITY")


def get_location_standard_locations(*, location: Location):
    """
    Return the standard django-cities locations for a given location.
    To do it it searches the django-cities tables with the location name and returns the most relevant result.
    """
    city = None
    subregion = None

    name = location.name.lower()
    city_name = name
    subregion_name = name

    if "," in name and name.endswith("provincia"):
        city_name = name.split(",")[0].strip()
        subregion_name = name.split(",")[1].strip()

    city = get_standard_city_from_city_name(city_name=city_name)

    if city:
        subregion = city.subregion
    else:
        subregion = get_standard_subregion_from_subregion_name(subregion_name=subregion_name)

    return city, subregion


def get_locations_for_search(*, search_text: str) -> list[LocationForSearch]:
    """
    Return a list of locations that match the given search text.
    """
    LOCATIONS_TO_RETURN = 10

    subregion_search = get_standard_locations_from_location_name(
        location_name=search_text,
        location_type=LocationTypes.SUBREGION,
        for_search=True,
    )
    city_search = get_standard_locations_from_location_name(
        location_name=search_text,
        location_type=LocationTypes.CITY,
        for_search=True,
    )

    subregion_search_count = min(subregion_search.count(), int(LOCATIONS_TO_RETURN / 2))
    city_search_count = min(city_search.count(), int(LOCATIONS_TO_RETURN / 2))

    subregions_to_return = LOCATIONS_TO_RETURN - city_search_count
    cities_to_return = LOCATIONS_TO_RETURN - subregion_search_count

    return [
        *[
            {"id": x.id, "name": x.name, "type": LocationTypes.SUBREGION}
            for x in subregion_search[:subregions_to_return]
        ],
        *[{"id": x.id, "name": x.name, "type": LocationTypes.CITY} for x in city_search[:cities_to_return]],
    ]
