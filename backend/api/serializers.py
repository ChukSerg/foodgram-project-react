from django.shortcuts import get_object_or_404
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Recipes, Ingredient, Tags, Structure, Favorite, ShoppingCart
from users.serializers import UserSerializer

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields = '__all__'


class StructureWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)


class StructureReadSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = Structure

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipesReadSerializer(serializers.ModelSerializer):

    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'author',
            'name',
            'image',
            'text',
            'id',
            'ingredients',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )
        read_only_fields = ['tags', 'author', 'name', 'image',
                            'text', 'id', 'ingredients', 'cooking_time']

    def get_image(self, obj):
        return obj.image.url

    def get_ingredients(self, obj):
        return StructureReadSerializer(obj.amount.all(), many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj,
                                           user=request.user).exists()


class RecipesWriteSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    ingredients = StructureWriteSerializer(many=True)
    author = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'name', 'image', 'text', 'ingredients', 'cooking_time')
    
    def to_representation(self, instance):
        serializer = RecipesReadSerializer(instance, context=self.context)
        return serializer.data
    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        author = serializers.CurrentUserDefault()(self)  
        new_recipe = Recipes.objects.create(author=author, **validated_data)
        new_recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(Ingredient, pk=ingredient.get('id'))
            Structure.objects.create(recipe=new_recipe, ingredient=current_ingredient, amount=ingredient.get('amount'))
        return new_recipe

    def update(self, recipe, validated_data):
        if "ingredients" in validated_data:
            ingredients = validated_data.pop("ingredients")
            recipe.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = get_object_or_404(
                    Ingredient, pk=ingredient.get('id'))
                Structure.objects.create(
                    recipe=recipe, ingredient=current_ingredient, amount=ingredient.get('amount'))
        tags = self.initial_data.pop("tags")
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id',)


class RecipeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
