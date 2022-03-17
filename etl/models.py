from typing import Optional

import mongoengine as me
from pydantic import BaseModel, Field

VALID_CAKE_FLAVORS = [
    "butter",
    "carrot",
    "black forest",
    "avocado",
    "vanilla",
    "caramel",
    "rainbow",
    "chiffon",
    "cream",
    "babka",
    "sponge",
    "apple",
    "strawberry",
    "biscuit",
    "chocolate",
]

VALID_UNITS = ["mm", "in", "m"]


class CakeMongoOrm(me.Document):
    """
    Mongoengine model of Cake document
    """

    entry_id = me.IntField(required=True, unique=True)
    name = me.StringField(null=True, choices=VALID_CAKE_FLAVORS)
    diameter_in_mm = me.FloatField(required=True)
    vegan = me.BooleanField(null=True)
    original_unit = me.StringField(choices=VALID_UNITS, required=True)


class CakeModel(BaseModel):
    """
    Pydantic model of a cake for data validation
    """

    entry_id: int = Field(description="The entry id of the cake")
    name: Optional[str] = Field(description="Name (or type) of the cake", default=None)
    diameter_in_mm: float = Field(description="Diameter of the cake in millimeters")
    vegan: Optional[bool] = Field(description="Specifies if cake is vegan or not", default=None)
    original_unit: str = Field(description="The original unit of cake's diameter")