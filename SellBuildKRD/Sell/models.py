from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Sell(models.Model):
    nameSell = models.TextField()
    specifications = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now=True)
    price = models.IntegerField()
    address = models.TextField(max_length=150)
    telephone = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell")

    # информация о квартире
    floor = models.IntegerField()
    totalFloor = models.IntegerField()
    numberOf_rooms = models.IntegerField()
    totalArea  = models.IntegerField()
    livingArea = models.IntegerField()
    kitchenArea = models.IntegerField()
    furnish = models.TextField(max_length=20)

