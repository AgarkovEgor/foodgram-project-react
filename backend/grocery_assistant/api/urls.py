from django.urls import path, include
from api.views import IngredientViewSet, TagViewSet, RecipeViewSet, UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet )
router.register(r'users',UserViewSet )

urlpatterns = [
    path('',include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
