from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from recipes import constants
from recipes.validators import WordNameValidator

User = get_user_model()


regex_validator = WordNameValidator()


class Ingredient(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_INGREDIENT,
                            verbose_name='Название инградиента',
                            help_text='Введите название ингредиента',
                            validators=[regex_validator])
    measurement_unit = models.CharField(
        max_length=constants.MAX_LENGTH_MEAS_UNIT,
        verbose_name='Единица измерения',
        help_text='Единицы измерения в метрической системе мер')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredients',
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tags(models.Model):
    name = models.CharField(max_length=constants.MAX_LENGTH_TAGS,
                            unique=True,
                            verbose_name='Название тега',
                            help_text='Введите название тега',
                            validators=[regex_validator])
    color = models.CharField(
        max_length=constants.MAX_LENGTH_TAGS_COLOR,
        unique=True,
        verbose_name='Цвет в HEX',
        help_text='Введите цвет тега в виде HEX-кода',
        validators=[RegexValidator(
            regex='^#([A-Fa-f0-9]{3,6})$',
            message='Введенное значение не является HEX-кодом!')]
    )
    slug = models.SlugField(
        max_length=constants.MAX_LENGTH_TAGS_SLUG,
        unique=True,
        verbose_name='Слаг',
        help_text='Введите короткое название тега',
        validators=[regex_validator]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Пользователь, написавший рецепт',
        related_name='recipe'
    )
    name = models.CharField(
        max_length=constants.MAX_LENGTH_RECIPES,
        unique=True,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
        validators=[regex_validator]
    )
    image = models.ImageField(
        verbose_name='Картинка блюда',
        upload_to='recipes/image/',
        help_text='Добавьте файл с изображением'
    )
    text = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tags, verbose_name='Теги')
    pub_date = models.DateTimeField(auto_now_add=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Время приготовления в минутах'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='amount')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='+'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество инградиентов',
        help_text='Введите количество инградиента в рецепте',
        validators=[
            MinValueValidator(1, message='Минимальное количество - 1')
        ]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient',),
                name='recipe_ingredient_exists'),
        )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} – {self.amount}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites')
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='+'
    )

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
        Recipes,
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:
        verbose_name = 'Лист покупок'
        verbose_name_plural = 'Листы покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
