# from pony.orm import Required

# from database import db


# class Condition(db.Entity):
#     # Table name
#     _table_ = "conditions"

#     # Attributes
#     source = Required(str, max_len=50)
#     change = Required(str, max_len=50)
#     value = Required(str, max_len=50)
#     unit = Required(str, max_len=50)

#     # Relations
#     indicator = Required("Indicator", unique=True)

from tortoise import fields, models


class ConditionModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Attributes
    source = fields.CharField(max_length=50)
    change = fields.CharField(max_length=50)
    value = fields.CharField(max_length=50)
    unit = fields.CharField(max_length=50)

    # Relationships
    indicator = fields.OneToOneField("models.IndicatorModel", related_name="condition")

    class Meta:
        table = "conditions"
