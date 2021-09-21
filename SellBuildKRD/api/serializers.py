from django.apps import apps
from rest_framework import serializers


class SellSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        fields = ("id", "nameSell", "specifications", "pub_date", "price", "address", "telephone", "author", "floor",
                  "totalFloor", "numberOf_rooms", "totalArea", "livingArea", "kitchenArea", "furnish", "type",
                  "status", "district", "published_tg")
        model = apps.get_model('Sell', 'Sell')


class SellSerializerAdd(serializers.ModelSerializer):
    nameSell = serializers.ReadOnlyField()
    pub_date = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField()
    class Meta:
        fields = ("nameSell", "specifications", "pub_date", "price", "address", "telephone", "author", "floor",
                  "totalFloor", "numberOf_rooms", "totalArea", "livingArea", "kitchenArea", "furnish", "type",
                  "status", "district", "published_tg")
        model = apps.get_model('Sell', 'Sell')
