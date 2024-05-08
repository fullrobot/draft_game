from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CardsConfig(AppConfig):
    name = "draft_game.apps.cards"
    verbose_name = _("Cards")
