from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from recipe.models import Recipe, Ingredient, Tag
from users.models import CustomUser

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        fields= ('id','email', 'username', 'first_name', 'last_name', ) #is_subscribed
        model = CustomUser

#Вопрос по полю author
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text', 'cooking_time',)
        model = Recipe

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient
        read_only_fileld = 'id', 'name', 'measurement_unit'      

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'colour', 'slug',)
        model = Tag        