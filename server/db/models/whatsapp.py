from tortoise import fields, models


class WhatsappModel(models.Model):
    # Fields
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    phone = fields.CharField(max_length=11, null=True)

    # Relationships
    user = fields.OneToOneField("models.UserModel", null=True, related_name="whatsapp")

    class Meta:
        table = "whatsapps"
