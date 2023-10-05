from datetime import timedelta

from django.utils.timezone import now

OFFER_WRITE_SERIALIZER_EXAMPLE = {
    "offer_id": "8731f0572f4404bcb1fdaeb10b55c2",
    "job": "Software developer",
    "status": "ACTIVE | NOT_ACTIVE | NO_STATUS | HTTP_ERROR | XPATH_ERROR",
    "url": "https://linkedin.com/offer/offer-id/",
    "source": "Linkedin",
    "company": {
        "name": "Connecthink",
        "is_competitor": True,
        "url": "https://linedin.com/connecthink/",
    },
    "temporality": "FULL_TIME | FULL_TIME_DEFAULT | PART_TIME | PART_TIME_DEFAULT",
    "attendance": "ON_SITE | ON_SITE_DEFAULT | REMOTE | REMOTE_DEFAULT | PARTIALLY_REMOTE | PARTIALLY_REMOTE_DEFAULT",
    "contract_type": "FIXED | FIXED_DEFAULT | TEMPORAL | TEMPORAL_DEFAULT | INTERNSHIP | INTERNSHIP_DEFAULT | FREELANCE | FREELANCE_DEFAULT | OTHERS | OTHERS_DEFAULT",
    "recruiter": "Xavier Velasco",
    "industry": "Tech",
    "location": "Sant Cugat del Vallès",
    "education_level": "Master's degree",
    "experience_level": "Senior",
    "skills": [
        "Python",
        "Javascript",
        "Leadership",
    ],
    "description": "Lorem ipsum",
    "posting_date": now(),
    "valid_until": now() + timedelta(days=30),
    "salary": {
        "min": 30_000,
        "max": 36_000,
    },
}

OFFER_AI_INFO_EXAMPLE = {
    "offer": "858c5577-53fa-47a3-a84c-986bd0345b09",
    "job_title": "Software developer",
    "description": "Lorem ipsum",
    "basic_taxonomy": "Lorem ipsum",
    "advanced_taxonomy": "Lorem ipsum",
    "salary": {
        "min": 30_000,
        "max": 36_000,
    },
    "location": "Sant Cugat del Vallès",
    "temporality": "FULL_TIME | PART_TIME",
    "attendance": "ON_SITE | REMOTE | PARTIALLY_REMOTE",
    "contract_type": "FIXED | TEMPORAL | INTERNSHIP | FREELANCE | OTHERS",
    "skills": [
        "Python",
        "Javascript",
        "Leadership",
    ],
}
