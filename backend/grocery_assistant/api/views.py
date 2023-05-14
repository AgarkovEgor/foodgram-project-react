from rest_framework import viewsets
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    TagSerializer,
)
from djoser.views import UserViewSet
from recipe.models import Recipe, Ingredient, Tag
from users.models import CustomUser


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer