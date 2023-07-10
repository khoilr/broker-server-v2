from tortoise import fields, models


class PredefinedParamModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    label = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    type = fields.CharField(max_length=32)
    # Relationship
    predefined_indicator = fields.ForeignKeyField("models.PredefinedIndicatorModel", related_name="predefined_params")
    params = fields.ReverseRelation["models.ParamModel"]

    class Meta:
        table = "predefined_params"
