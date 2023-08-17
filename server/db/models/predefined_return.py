from tortoise import fields, models


class PredefinedReturnModel(models.Model):
    """Data model for predefined return."""

    # Fields
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    label = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Relationship
    predefined_indicator = fields.ForeignKeyField(
        "models.PredefinedIndicatorModel",
        related_name="predefined_returns",
    )

    class Meta:
        table = "predefined_returns"
