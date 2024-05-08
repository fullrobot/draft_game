from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from draft_game.apps.cards.api.views import CardViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("cards", CardViewSet)


app_name = "api"
urlpatterns = router.urls
