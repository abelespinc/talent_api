from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Literal

from django.contrib.postgres.search import SearchQuery
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.utils.text import slugify

from talent.core.services.dates import get_date_range_for_filtering
from talent.jobs.utils import LocationTypes
from talent.offers.models import Offer
from talent.offers.models import OfferDuplicate
from talent.offers.utils import OfferStatus

if TYPE_CHECKING:
    from django.db.models import QuerySet


OfferAiField = Literal[
    "salary",
    "location",
    "temporality",
    "attendance",
    "contract_type",
    "skills",
]


def filter_offers_by_title_or_description(
    offers: QuerySet[Offer],
    search: str,
    by_title=True,
    by_description=True,
) -> QuerySet[Offer]:
    if (" or " in search.lower()) or ('"' in search):
        search_query = SearchQuery(search, search_type="websearch")
    else:
        search_query = SearchQuery(search)

    search_by_title_offers = offers.annotate(search_vector=SearchVector("job__name")).filter(search_vector=search_query)
    search_by_description_offers = offers.filter(description_search_vector=search_query)

    if by_title and by_description:
        return search_by_title_offers | search_by_description_offers
    elif by_title:
        return search_by_title_offers
    elif by_description:
        return search_by_description_offers
    else:
        raise ValueError("At least one of by_title or by_description must be True")


def get_filtered_offers(*, params: dict, initial_qs: QuerySet = None):
    # Use if/else instead of or because we don't want to evaluate the qs
    offers = initial_qs if initial_qs is not None else Offer.objects.all()

    filters = {}

    job = params.get("job")
    status = params.get("status")
    location_id = params.get("locationId")
    location_type = params.get("locationType")
    temporality = params.get("temporality")
    attendance = params.get("attendance")
    contract_type = params.get("contractType")
    only_competitors = params.get("competitor")
    posting_date = params.get("postingDate")
    company = params.get("company")
    duplicates = params.get("duplicates")
    min_salary = params.get("minSalary")
    title_and_description = params.get("titleAndDescription")

    filters = Q(is_active=True)

    if job:
        if not title_and_description:
            offers = filter_offers_by_title_or_description(offers, job)
        elif title_and_description == "ONLY_TITLE":
            offers = filter_offers_by_title_or_description(offers, job, by_description=False)
        elif title_and_description == "ONLY_DESCRIPTION":
            offers = filter_offers_by_title_or_description(offers, job, by_title=False)

    if status:
        filters &= Q(status=status)
    else:
        filters &= Q(status=OfferStatus.ACTIVE)

    if location_id and location_type:
        if location_type == LocationTypes.CITY:
            filters &= Q(location__city__pk=location_id)
        elif location_type == LocationTypes.SUBREGION:
            filters &= Q(location__subregion__pk=location_id)
        else:
            raise ValueError(f"Invalid location type: {location_type}")
    if temporality:
        filters &= (
            Q(temporality__name=temporality)
            | Q(temporality__name=f"{temporality}_DEFAULT")
            | Q(ai_info__temporality__name=temporality)
            | Q(ai_info__temporality__name=f"{temporality}_DEFAULT")
        )
    if attendance:
        filters &= (
            Q(attendance__name=attendance)
            | Q(attendance__name=f"{attendance}_DEFAULT")
            | Q(ai_info__attendance__name=attendance)
            | Q(ai_info__attendance__name=f"{attendance}_DEFAULT")
        )
    if contract_type:
        filters &= (
            Q(contract_type__name=contract_type)
            | Q(contract_type__name=f"{contract_type}_DEFAULT")
            | Q(ai_info__contract_type__name=contract_type)
            | Q(ai_info__contract_type__name=f"{contract_type}_DEFAULT")
        )
    if only_competitors:
        filters &= Q(company__is_competitor=only_competitors == "true")
    if company:
        filters &= Q(company__slug__icontains=slugify(company))
    if posting_date:
        filters &= Q(posting_date__date__range=get_date_range_for_filtering(date_filter=posting_date))
    if duplicates:
        filters &= Q(duplicates__isnull=duplicates == "NO")
    if min_salary:
        filters &= Q(salary__max__gte=int(min_salary)) | Q(ai_info__salary__max__gte=int(min_salary))

    return offers.filter(filters)


def get_offer_similarities(*, offer: Offer):
    offer_duplicates = OfferDuplicate.objects.filter(Q(from_offer=offer) | Q(to_offer=offer))
    duplicate = offer_duplicates.first() if offer_duplicates.exists() else None

    return {
        "job": duplicate.job_title_similarity if duplicate else None,
        "description": duplicate.description_similarity if duplicate else None,
        "contract_type": duplicate.contract_type_similarity if duplicate else None,
        "temporality": duplicate.temporality_similarity if duplicate else None,
        "location": duplicate.location_similarity if duplicate else None,
        "attendance": duplicate.attendance_similarity if duplicate else None,
    }


def get_offer_salary(*, offer: Offer):
    salary = {"min": None, "max": None, "is_ai": False}
    offer_salary = offer.salary
    offer_has_salary = offer_salary["min"] or offer_salary["max"]

    if offer_has_salary:
        salary.update(offer_salary)
    else:
        offer_has_ai_info = hasattr(offer, "ai_info")
        offer_ai_salary = offer_has_ai_info and offer.ai_info.salary
        offer_ai_info_has_salary = offer_ai_salary and (offer_ai_salary["min"] or offer_ai_salary["max"])

        if offer_ai_info_has_salary:
            salary.update(offer_ai_salary)
            salary["is_ai"] = True

    return salary


def get_offer_info_field(*, offer: Offer, field: OfferAiField):
    if field == "salary":
        return get_offer_salary(offer=offer)

    info = getattr(offer, field, None)
    offer_has_ai_info = hasattr(offer, "ai_info")

    if not info and offer_has_ai_info:
        info = getattr(offer.ai_info, field, None)

    return info
