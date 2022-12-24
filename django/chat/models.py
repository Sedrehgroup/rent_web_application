from django.db import models
from django.utils.timezone import now

from config import settings
from property.models import Property

User = settings.AUTH_USER_MODEL


class Chat(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenant")
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publisher", blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.pk:
            # on_create
            self.publisher = self.property.owner
        super(Chat, self).save(*args, **kwargs)


class Note(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=now)

