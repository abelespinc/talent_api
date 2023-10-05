from django.conf import settings
from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from talent.companies.api.views import CompanyViewSet
from talent.companies.api.views import IndustryViewSet
from talent.core.api.views import ConfigurationViewSet
from talent.jobs.api.views import AttendanceViewSet
from talent.jobs.api.views import ContractTypeViewSet
from talent.jobs.api.views import EducationLevelViewSet
from talent.jobs.api.views import ExperienceLevelViewSet
from talent.jobs.api.views import LocationViewSet
from talent.jobs.api.views import SkillViewSet
from talent.jobs.api.views import TemporalityViewSet
from talent.offers.api.views import OfferAiInfoViewSet
from talent.offers.api.views import OfferDuplicateViewSet
from talent.offers.api.views import OfferViewSet
from talent.offers.api.views import RecruiterViewSet
from talent.offers.api.views import SourceViewSet
from talent.users.api.views import LoginViewSet
from talent.users.api.views import RegisterViewSet
from talent.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Core
router.register("configuration", ConfigurationViewSet)
# Companies
router.register("companies", CompanyViewSet)
router.register("industry", IndustryViewSet)
# Jobs
router.register("temporalities", TemporalityViewSet)
router.register("attendances", AttendanceViewSet)
router.register("contract-types", ContractTypeViewSet)
router.register("experience-levels", ExperienceLevelViewSet)
router.register("education-levels", EducationLevelViewSet)
router.register("skills", SkillViewSet)
router.register("locations", LocationViewSet)
# Offers
router.register("offers/ai-info", OfferAiInfoViewSet)
router.register("offers/duplicates", OfferDuplicateViewSet)
router.register("offers", OfferViewSet)
router.register("sources", SourceViewSet)
router.register("recruiters", RecruiterViewSet)
# Users
router.register("users/register", RegisterViewSet)
router.register("users", UserViewSet)


app_name = "api"
urlpatterns = [
    path("users/login/", LoginViewSet.as_view(), name="login"),
] + router.urls
