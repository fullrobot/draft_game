from rest_framework.viewsets import ModelViewSet

from draft_game.apps.cards.models import Card

from .serializers import CardSerializer


class CardViewSet(ModelViewSet):
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    lookup_field = "pk"
