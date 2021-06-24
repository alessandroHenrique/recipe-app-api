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


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = models.Recipe
        fields = (
            'id',
            'title',
            'ingredients',
            'tags',
            'time_minutes',
            'price',
            'link',
        )
