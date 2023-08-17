from tortoise import fields, models


class PredefinedIndicatorModel(models.Model):
    """Data model for predefined Indicator."""

    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    name = fields.CharField(max_length=200, unique=True)
    label = fields.CharField(max_length=200)

    # Relationships
    predefined_returns = fields.ReverseRelation["models.PredefinedReturnModel"]
    predefined_params = fields.ReverseRelation["models.PredefinedParamModel"]
    indicators = fields.ReverseRelation["models.IndicatorModel"]

    class Meta:
        table = "predefined_indicators"
