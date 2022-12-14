# Generated by Django 2.2.19 on 2022-12-12 08:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221212_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipes'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Запрещенные символы в названии', regex='^[а-яА-ЯёЁa-zA-Z0-9 \\-]+$')], verbose_name='Название инградиента'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipes'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingridient_recipe', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(message='Запрещенные символы в названии', regex='^[а-яА-ЯёЁa-zA-Z0-9 \\-]+$')], verbose_name='Название тега'),
        ),
    ]
