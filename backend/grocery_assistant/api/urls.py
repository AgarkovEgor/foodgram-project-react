from django.urls import path, include
from api.views import IngredientViewSet, TagViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('',include(router.urls))
]
