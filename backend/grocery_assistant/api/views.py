from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from core.pagination import CustomPageNumberPagination
from .serializers import (
    RecipeSerializer,
    IngredientSerializer,
    TagSerializer,
    FollowSerializer,
    UserSerializers,
    ShoppingCartSerializer,
    FavoriteSerializer
)
from djoser.views import UserViewSet
from recipe.models import Recipe, Ingredient, Tag, ShoppingCart, Favorite
from users.models import CustomUser,Follow


class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class=UserSerializers
    pagination_class = CustomPageNumberPagination

    @action(["GET"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
    @action(methods=['GET'],detail=False,permission_classes=[IsAuthenticated])
    def subscriptions(self,request,*args,**kwargs):
        author_id = request.user.follower.values_list('author_id',flat=True) 
        print(author_id)
        queryset = CustomUser.objects.filter(id__in=author_id) 
        page=self.paginate_queryset(queryset)
        serializer = FollowSerializer(page,many=True,context=self.get_serializer_context())
        return self.get_paginated_response(serializer.data)
    
    @action(methods=['POST','DELETE'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self,request,*args,**kwargs):
        user = request.user
        author = get_object_or_404(CustomUser,pk=kwargs.get('id'))
        if request.method == 'POST':
            serializer = FollowSerializer(author,data=request.data,context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user,author=author)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        if not Follow.objects.filter(user=user,author=author).exists():
            return Response({"errors": "Вы не подписаны на этого пользователя"},status=status.HTTP_400_BAD_REQUEST)
        follow = get_object_or_404(Follow, author=author,user=user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST','DELETE'],
        permission_classes=[IsAuthenticated])
    def shopping_cart(self,request,*args,**kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs.get('id'))
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(recipe,data=request.data,context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            ShoppingCart.object.create(user=user,recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        shopping_cart = get_object_or_404(ShoppingCart,user=user,recipe=recipe)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=True,
        methods=['POST','DELETE'],
        permission_classes=[IsAuthenticated])
    def favorite(self,request,*args,**kwargs):
        user = request.user
        recipe = get_object_or_404(Recipe, id=kwargs.get('id'))
        if request.method == 'POST':
            serializer = FavoriteSerializer(recipe,data=request.data,context=self.get_serializer_context())
            serializer.is_valid(raise_exception=True)
            Favorite.object.create(user=user,recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        favarite_recipe = get_object_or_404(Favorite,user=user,recipe=recipe)
        favarite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer