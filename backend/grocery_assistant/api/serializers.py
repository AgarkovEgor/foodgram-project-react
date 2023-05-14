from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipe.models import Recipe, Ingredient, Tag, IngredientRecipe
from users.models import CustomUser, Follow

class UserSerializers(serializers.ModelSerializer):
    is_subscribed =  serializers.SerializerMethodField()
    class Meta:
        fields= ('id','email', 'username', 'first_name', 'last_name', 'is_subscribed',)
        model = CustomUser

    def get_is_subscribed(self,obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    class Meta:
        fields = ('id','amount',)
        model = IngredientRecipe


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializers(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True) 
    image = Base64ImageField()
    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients','image', 'name', 'text', 'cooking_time',)
        model = Recipe

    def create(self,data):
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        recipe = Recipe.objects.create(**data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(recipe=recipe,ingredient=ingredient.get('id'),amount=ingredient.get('amount'))
        return recipe

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient
        read_only_fileld = 'id', 'name', 'measurement_unit'      

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'colour', 'slug',)
        model = Tag        

        