from tortoise import fields, models


class StockModel(models.Model):
    """Data model for stock."""

    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Attributes
    market = fields.CharField(max_length=10)
    symbol = fields.CharField(max_length=10)
    name = fields.CharField(max_length=256, null=True)
    en_name = fields.CharField(max_length=256, null=True)

    # Relationships
    strategies = fields.ReverseRelation["models.StrategyModel"]

    class Meta:
        table = "stocks"
        unique_together = (("market", "symbol"),)
