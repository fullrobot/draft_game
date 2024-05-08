from django.db import models
from model_utils.models import TimeStampedModel


class CardType(TimeStampedModel):
    """
    Model to represent Card Types
    """

    label = models.CharField(
        max_length=255,
        unique=True,
        help_text="Card Type label",
    )

    class Meta:
        verbose_name = "Card Type"
        verbose_name_plural = "Card Types"

    def __str__(self):
        return self.label


class EffectType(TimeStampedModel):
    """
    Model to represent Effect Types
    """

    label = models.CharField(
        max_length=255,
        help_text="Effect Type label",
    )
    cost = models.CharField(
        max_length=50,
        blank=True,
        help_text="Effect Cost",
    )

    class Meta:
        verbose_name = "Effect Type"
        verbose_name_plural = "Effect Types"
        unique_together = ("label", "cost")

    def __str__(self):
        if self.cost:
            return f"{self.label}: {self.cost}"
        return self.label


class CardEffect(TimeStampedModel):
    """
    Model to represent Card Effects
    """

    effect_types = models.ManyToManyField(
        "cards.EffectType",
        related_name="effect_type",
        help_text="Card Effect - Effect Type relation",
    )
    effect_text = models.CharField(
        max_length=1000,
        help_text="Card Effect text description",
    )

    class Meta:
        verbose_name = "Card Effect"
        verbose_name_plural = "Card Effects"

    def __str__(self):
        return self.effect_text


class Card(TimeStampedModel):
    """
    Model to represent Draft Game Card
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of Card",
    )
    value = models.SmallIntegerField(
        help_text="Point value of Card",
    )
    card_type = models.ForeignKey(
        "cards.CardType",
        related_name="card_type",
        on_delete=models.PROTECT,
        help_text="Card - Card Type relation",
    )
    effect = models.ForeignKey(
        "cards.CardEffect",
        related_name="card_effect",
        on_delete=models.PROTECT,
        help_text="Card - Card Effect relation",
    )

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return self.name
