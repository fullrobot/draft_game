from django.contrib import admin

from .models import Card
from .models import CardEffect
from .models import CardType
from .models import EffectType


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    fields = ["label"]
    search_fields = ["label"]
    list_display = ["label"]


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = [
        "name",
        "value",
        "card_type",
        "effect",
    ]
    search_fields = ["name"]
    list_display = [
        "name",
        "value",
        "card_type",
        "effect",
    ]


@admin.register(CardEffect)
class CardEffectAdmin(admin.ModelAdmin):
    fields = [
        "effect_types",
        "effect_text",
    ]
    search_fields = [
        "effect_text",
    ]
    list_display = [
        "effect_text",
    ]


@admin.register(EffectType)
class EffectTypeAdmin(admin.ModelAdmin):
    fields = [
        "label",
        "cost",
    ]
    search_fields = ["label"]
    list_display = [
        "label",
        "cost",
    ]
