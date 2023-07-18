from tortoise import fields, models


class ConditionModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Attributes
    source = fields.CharField(max_length=50)
    change = fields.CharField(max_length=50)
    value = fields.FloatField()
    unit = fields.CharField(max_length=50)

    # Relationships
    indicator = fields.OneToOneField("models.IndicatorModel", related_name="condition")

    class Meta:
        table = "conditions"
