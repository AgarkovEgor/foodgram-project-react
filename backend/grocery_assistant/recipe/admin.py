from django.contrib import admin

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "colour", "slug")
    search_fields = ("name", "colour", "slug")
    list_filter = ("name", "colour", "slug")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name", "measurement_unit")
    list_filter = ("name", "measurement_unit")


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "text", "cooking_time", "image", "pub_date")
    search_fields = ("name", "author", "text", "cooking_time")
    list_filter = ("name", "author", "tags")
    readonly_fields = ("favarite_count",)

    def favarite_count(self, obj):
        return obj.favorites.count()


class IngridientsRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")
    search_fields = ("recipe", "ingredient")
    list_filter = ("recipe", "ingredient")


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = (
        "user",
        "recipe",
    )


class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = (
        "user",
        "recipe",
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngridientsRecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavouriteAdmin)
