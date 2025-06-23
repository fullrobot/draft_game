from typing import Literal

from app.core.filter import Filter


class CardFilter(Filter):
    order_by: Literal["id", "name", "card_type", "value"] = "id"
