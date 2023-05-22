from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="recipe/images/")  # TODO upload to
    text = models.TextField()
    ingredients = models.ManyToManyField(
        "Ingredient", related_name="recipes", through="IngredientRecipe"
    )
    tags = models.ManyToManyField("Tag", related_name="recipes")
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    colour = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=10)


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredient_recipe"
    )

    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredient_recipe"
    )
    amount = models.PositiveIntegerField()


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, related_name="carts", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="carts", on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            ),
        )

    # TODO валидация на уровне модели


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name="favorites", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="favorites", on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "recipe"), name="unique_favorite"),
        )

    # TODO валидация на уровне модели
