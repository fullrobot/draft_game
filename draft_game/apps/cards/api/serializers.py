from rest_framework import serializers

from draft_game.apps.cards.models import Card
from draft_game.apps.cards.models import CardEffect


class CardEffectSerializer(serializers.ModelSerializer[CardEffect]):
    effect_types = serializers.StringRelatedField(many=True)

    class Meta:
        model = CardEffect
        fields = [
            "effect_types",
            "effect_text",
        ]


class CardSerializer(serializers.ModelSerializer[Card]):
    card_type = serializers.StringRelatedField()
    effect = CardEffectSerializer()

    class Meta:
        model = Card
        fields = [
            "name",
            "value",
            "effect",
            "card_type",
        ]
