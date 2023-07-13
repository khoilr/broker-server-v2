from tortoise import fields, models


class DummyModel(models.Model):
    """Model for demo purpose."""

    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
