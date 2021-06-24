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
        # read_only=True
        queryset=models.Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        # read_only=True
        queryset=models.Tag.objects.all()
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


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
