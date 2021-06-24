from rest_framework import serializers

from core import models


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = models.Tag
        fields = ('id', 'name')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    class Meta:
        model = models.Ingredient
        fields = ('id', 'name')
