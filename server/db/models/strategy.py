from tortoise import fields, models


class StrategyModel(models.Model):
    """Data model for strategy."""

    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    notified = fields.BooleanField(null=True)

    # Relationships
    user = fields.ForeignKeyField("models.UserModel", related_name="strategies")
    stocks = fields.ManyToManyField("models.StockModel", related_name="strategies")
    indicators = fields.ReverseRelation["models.IndicatorModel"]

    class Meta:
        table = "strategies"
