from django.urls import include, path
from rest_framework import routers

from api.views import RecipesViewSet, TagsViewSet, IngredientViewSet
from users.views import CustomUserViewSet


router = routers.DefaultRouter()
router.register('recipes', RecipesViewSet, basename="recipes")
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
