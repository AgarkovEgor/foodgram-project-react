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
    pub_date = models.DateTimeField(verbose_name="Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name} ({self.author})"


class Tag(models.Model):
    name = models.CharField("Название тэга", max_length=200)
    slug = models.SlugField("Адрес тэга", unique=True, max_length=200)
    colour = models.CharField("Цвет(HEX)", max_length=7, default="2c3cba")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name}"


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

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = (
            models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="ingredient_in_recipe_repetition"
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, related_name="carts", on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name="carts", on_delete=models.CASCADE)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            ),
        )

    


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

    
