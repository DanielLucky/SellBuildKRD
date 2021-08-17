from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactSend(models.Model):
    name_agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ContactSend")
    theme = models.TextField(max_length=250)
    message = models.TextField()
