from django.db import models
from model_utils.models import TimeStampedModel


class Card(TimeStampedModel):
    """
    Model to represent Draft Game Card
    """

    name = models.CharField(max_length=255, unique=True, help_text="Name of Card")
