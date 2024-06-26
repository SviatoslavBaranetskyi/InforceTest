from rest_framework import serializers
from .models import Restaurant, Menu, Item


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ['restaurant']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ['menu']
