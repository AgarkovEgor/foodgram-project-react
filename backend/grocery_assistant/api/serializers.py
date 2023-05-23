from drf_extra_fields.fields import Base64ImageField
from recipe.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from users.models import CustomUser, Follow


class UserSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )
        model = CustomUser

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
        model = IngredientRecipe

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["id"] = instance.ingredient.id
        return data


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializers(read_only=True)
    ingredients = IngredientAmountSerializer(many=True, source="ingredient_recipe")
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "image",
            "name",
            "text",
            "cooking_time",
            "is_favorite",
            "is_in_shopping_cart",
        )
        model = Recipe

    def create(self, data):
        ingredients = data.pop("ingredient_recipe")
        tags = data.pop("tags")
        recipe = Recipe.objects.create(**data)
        recipe.tags.set(tags)
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient["id"],
                    amount=ingredient["amount"],)
                
                for ingredient in ingredients]
            )
              
        return recipe

    def get_is_favorite(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return obj.carts.filter(user=request.user).exists()

    def to_representation(self, instance):
        self.fields["tags"] = TagSerializer(many=True)
        return super().to_representation(instance)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
        model = Ingredient
        read_only_fileld = "id", "name", "measurement_unit"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "name",
            "colour",
            "slug",
        )
        model = Tag


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(default=True)
    recipes_count = serializers.IntegerField(source="recipes.count", read_only=True)
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("email", "username", "first_name", "last_name")

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = ShortRecipeSerializer(recipes, many=True, context=self.context)
        return serializer.data

    def validate(self, data):
        author = self.instance
        user = self.context.get("request").user
        if CustomUser.follower(author=author).exists():
            raise ValidationError(
                detail="Попытка повторной подписки",
                code=status.HTTP_400_BAD_REQUEST,
            )
        elif user == author:
            raise ValidationError(
                detail="Попытка подписки на самого себя",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class ShoppingCartFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "name", "image", "cooking_time")
        model = Recipe
        read_only_fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        recipe = self.instance
        user = self.context.get("request").user
        if CustomUser.carts.filter(recipe=recipe).exists():
            raise ValidationError(
                detail="Этот рецепт уже добавлен",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
