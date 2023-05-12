from django.urls import path, include
from api.views import IngredientViewSet, TagViewSet, RecipeViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet )

urlpatterns = [
    path('',include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
