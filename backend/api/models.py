from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название инградиента')
    measurement_unit = models.CharField(
        max_length=16, verbose_name='Единица измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название тега')
    color = models.CharField(max_length=7, unique=True, verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return self.slug


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор рецепта')
    name = models.CharField(max_length=150, unique=True, verbose_name='Название рецепта')
    image = models.ImageField(verbose_name='Картинка блюда', upload_to='recipes/')
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='Structure', related_name='recipes', verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tags, verbose_name='Теги')
    pub_date = models.DateTimeField(auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время приготовления в минутах')
    
    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Structure(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='amount')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='amount')
    amount = models.PositiveIntegerField(verbose_name='Количество инградиентов')

    class Meta:
        default_related_name = 'ingridient_recipe'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='recipe_ingredient_exists'),
            models.CheckConstraint(
                check=models.Q(amount__gte=1),
                name='amount_gte_1'),
        )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorites',
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart')
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, related_name='shopping_cart')

    class Meta:
        verbose_name = 'Лист покупок'
        verbose_name_plural = 'Листы покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
