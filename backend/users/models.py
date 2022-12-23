from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint
from django.core.validators import RegexValidator

from users.validators import check_username
from users.constants import MAX_LENGTH_USER
from foodgram_project import settings
from users.validators import UserNameValidator

regex_validator = UserNameValidator()


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(max_length=settings.MAX_LENGTH_EMAIL,
                              unique=True,
                              verbose_name='Электронная почта',
                              help_text='Введите e-mail')
    first_name = models.CharField(max_length=MAX_LENGTH_USER,
                                  verbose_name='Имя',
                                  help_text='Введите свое имя',
                                  validators=[regex_validator])
    last_name = models.CharField(max_length=MAX_LENGTH_USER,
                                 verbose_name='Фамилия',
                                 help_text='Введите свою фамилию',
                                 validators=[regex_validator])
    password = models.CharField(max_length=MAX_LENGTH_USER,
                                verbose_name='Пароль для входа',
                                help_text='Придумайте пароль')
    username = models.CharField(
        max_length=MAX_LENGTH_USER, unique=True,
        verbose_name='Имя пользователя',
        help_text='Придумайте никнейм',
        validators=[check_username,
                    RegexValidator(regex=r'^[\w.@+-]+$',
                                   message='Запрещенные символы в имени')])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            CheckConstraint(
                name="Ограничение на самоподписку",
                check=~models.Q(user=models.F('author')),
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
