from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r"ingredients", IngredientViewSet)
router.register(r"tags", TagViewSet)
router.register(r"recipes", RecipeViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
