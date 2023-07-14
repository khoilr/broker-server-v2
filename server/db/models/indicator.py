from tortoise import fields, models


class IndicatorModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relationships
    strategy = fields.ForeignKeyField("models.StrategyModel", related_name="indicators")
    predefined_indicator = fields.ForeignKeyField(
        "models.PredefinedIndicatorModel",
        related_name="indicators",
    )
    params = fields.ReverseRelation["models.ParamModel"]
    condition = fields.ReverseRelation["models.ConditionModel"]

    class Meta:
        table = "indicators"
