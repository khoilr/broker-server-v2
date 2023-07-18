from tortoise import fields, models


class ParameterModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Attributes
    value = fields.CharField(max_length=50)

    # Relationships
    indicator = fields.ForeignKeyField(
        "models.IndicatorModel",
        related_name="parameters",
    )
    predefined_param = fields.ForeignKeyField(
        "models.PredefinedParamModel",
        related_name="parameters",
    )

    class Meta:
        table = "parameters"
