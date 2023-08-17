from tortoise import fields, models


class TelegramModel(models.Model):
    """Data model for telegram account."""

    # Fields
    _id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Telegram Fields
    username = fields.CharField(max_length=200, unique=True, null=True)
    first_name = fields.CharField(max_length=200, null=True)
    last_name = fields.CharField(max_length=200, null=True)
    is_bot = fields.BooleanField(null=True)
    id = fields.CharField(max_length=200, null=True)
    language_code = fields.CharField(max_length=200, null=True)
    can_join_groups = fields.BooleanField(null=True)
    can_read_all_group_messages = fields.BooleanField(null=True)
    supports_inline_queries = fields.BooleanField(null=True)
    is_premium = fields.BooleanField(null=True)
    added_to_attachment_menu = fields.BooleanField(null=True)

    # Relationships
    user = fields.OneToOneField("models.UserModel", null=True, related_name="telegram")

    class Meta:
        table = "telegrams"
