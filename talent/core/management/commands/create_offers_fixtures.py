import random
import uuid
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from faker import Faker

from talent.jobs.utils import Attendances
from talent.jobs.utils import ContractTypes
from talent.jobs.utils import Temporalities
from talent.offers.api.serializers import OfferDuplicateSerializer
from talent.offers.api.serializers import OfferWriteSerializer
from talent.offers.models import Offer
from talent.offers.models import Source

OFFERS_TO_CREATE = 10_000
SOURCES = ["Linkedin", "Indeed", "Infoempleo", "Infojobs"]
INDUSTRIES = [
    "Tecnológica",
    "Farmacéutica",
    "Constructora",
    "Textil",
    "Energética",
    "Metalúrgica",
    "Química",
    "Agricultura",
    "Hostelería",
]
EDUCATION_LEVELS = [
    "Educación secundaria",
    "Ciclo formativo (medio)",
    "Ciclo formativo (superior)",
    "Grado",
    "Máster",
    "Doctorado",
]
EXPERIENCE_LEVELS = ["Entry", "Junior", "Mid-level", "Senior", "Staff"]
SKILLS = [
    "Python",
    "Django",
    "Javascript",
    "Vue",
    "Angular",
    "React",
    "Java",
    "Power BI",
    "Tableau",
    "Excel",
    "PowerPoint",
    "Spark",
    "SQL",
    "MongoDB",
    "Liderazgo de equipos",
    "Google Analytics",
    "Edición de vídeo",
    "Manejo de RRSS",
]
SALARIES = [*range(14_000, 62_000, 2_000), None]
SALARY_VARIATION = [500, 1_000, 1_500, 2_000, 4_000, 5_000, 6_000, 8_000, 10_000]

companies = ["Connecthink"]  # Will be populated while creating offers
start_posting_date = make_aware(datetime(2022, 1, 1, 0, 0, 0, 0))


class Command(BaseCommand):
    help = "Fills db with fake offers"
    fake = Faker("es-ES")

    def get_random_salary(self):
        min_salary = random.choice(SALARIES)
        salary_variation = random.choice(SALARY_VARIATION)
        max_salary = min_salary + salary_variation if min_salary else None
        max_salary = random.choice([*([max_salary] * 10), None])

        return {"min": min_salary, "max": max_salary}

    def create_offer_duplicate(self, offer: Offer):
        original_offer_pk = offer.pk
        offer.pk = None
        offer.offer_id = uuid.uuid4()
        offer._state.adding = True

        if Source.objects.count() > 1:
            offer.source = random.choice(Source.objects.exclude(pk=offer.source.pk))

        offer.save()

        serializer = OfferDuplicateSerializer(
            data={
                "from_offer": original_offer_pk,
                "to_offer": offer.pk,
                "job_title_similarity": int(random.random() * 100),
                "description_similarity": int(random.random() * 100),
                "contract_type_similarity": int(random.random() * 100),
                "temporality_similarity": int(random.random() * 100),
                "location_similarity": int(random.random() * 100),
                "attendance_similarity": int(random.random() * 100),
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.instance

    def create_offer(self):
        serializer = OfferWriteSerializer(
            data={
                "offer_id": str(uuid.uuid4()),
                "job": self.fake.job(),
                "url": "https://example.com/offers/offer-id/",
                "source": random.choice(SOURCES),
                "company": {
                    "name": random.choice([random.choice(companies), self.fake.company()]),
                    "url": "https://linkedin.com/company/profile/",
                    "is_competitor": random.choice([*([False] * 20), True]),  # 1 out of 20 will be competitors
                },
                "temporality": random.choice([value for value in Temporalities.values if value]),
                "attendance": random.choice([value for value in Attendances.values if value]),
                "contract_type": random.choice([value for value in ContractTypes.values if value]),
                "recruiter": self.fake.name(),
                "industry": random.choice(INDUSTRIES),
                "location": self.fake.city(),
                "education_level": random.choice(EDUCATION_LEVELS),
                "experience_level": random.choice(EXPERIENCE_LEVELS),
                "skills": random.choices(SKILLS, k=random.randint(1, 5)),
                "description": self.fake.paragraph(nb_sentences=10),
                "posting_date": self.fake.date_time_this_year(before_now=True, after_now=False),
                "valid_until": self.fake.date_time_this_year(before_now=False, after_now=True),
                "salary": self.get_random_salary(),
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 50% chance to create a duplicate
        if random.random() > 0.5:
            self.create_offer_duplicate(offer=serializer.instance)

            # 30% chance to create a second duplicate
            if random.random() > 0.7:
                self.create_offer_duplicate(offer=serializer.instance)

                # 10% chance to create a third duplicate
                if random.random() > 0.9:
                    self.create_offer_duplicate(offer=serializer.instance)

    def handle(self, *args, **options):
        for _ in range(OFFERS_TO_CREATE):
            self.create_offer()
