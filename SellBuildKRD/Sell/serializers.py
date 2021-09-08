from rest_framework import serializers

from .models import Sell


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("nameSell", "specifications", "pub_date", "price", "address", "telephone", "author", "floor",
                  "totalFloor", "numberOf_rooms", "totalArea", "livingArea", "kitchenArea", "furnish", "type",
                  "status", "district", "published_tg")
        model = Sell
