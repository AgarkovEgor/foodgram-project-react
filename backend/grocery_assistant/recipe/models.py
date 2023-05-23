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
    name = models.CharField(
        max_length=50,
        verbose_name="Название рецепта"
    )
    image = models.ImageField(
        upload_to="recipe/images/",
        verbose_name="Изображение рецепта"
    )  
    text = models.TextField(verbose_name="Текст рецепта")
    ingredients = models.ManyToManyField(
        "Ingredient", 
        related_name="recipes", 
        through="IngredientRecipe",
        verbose_name="Ингредиенты для рецепта"
    )
    tags = models.ManyToManyField(
        "Tag", 
        related_name="recipes",
        verbose_name="Тег рецепта")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления"
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", 
        auto_now_add=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return f"{self.name} ({self.author})"


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название тэга", 
        max_length=200
    )
    slug = models.SlugField(
        verbose_name="Адрес тэга",
        unique=True, 
        max_length=200
    )
    colour = models.CharField(
        verbose_name="Цвет(HEX)",
        max_length=7, 
        default="2c3cba"
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name}"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, 
        related_name="ingredient_recipe",
        verbose_name="Рецепт"
    )

    ingredient = models.ForeignKey(
        Ingredient, 
        on_delete=models.CASCADE, 
        related_name="ingredient_recipe",
        verbose_name="Ингредиент"
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество ингредиента"
    )

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = (
            models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="ingredient_in_recipe_repetition"
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        related_name="carts", 
        on_delete=models.CASCADE,
        verbose_name = "Пользователь")
    recipe = models.ForeignKey(
        Recipe, 
        related_name="carts", 
        on_delete=models.CASCADE,
        verbose_name="Покупка")

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_shopping_cart"
            ),
        )
        ordering = ['-id']

    def __str__(self):
        return (f'Пользователь {self.user} '
                f'добавил {self.recipe} в покупки.')

    


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        related_name="favorites", 
        on_delete=models.CASCADE,
        verbose_name = "Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe, 
        related_name="favorites", 
        on_delete=models.CASCADE,
        verbose_name="Избранный Рецепт"

    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=("user", "recipe"), name="unique_favorite"),
        )
    def __str__(self):
        return (f'Пользователь {self.user} '
                f'добавил {self.recipe} в избранное.')
    
