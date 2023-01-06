from django_filters import rest_framework as drf
from recipes.models import Ingredient


class IngredientFilter(drf.FilterSet):
    """Фильтр ингредиентов"""
    name = drf.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
