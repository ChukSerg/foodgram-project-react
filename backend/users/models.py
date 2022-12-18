from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import RegexValidator

from users.validators import check_username
from users import constants


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(max_length=constants.MAX_LENGTH_EMAIL,
                              unique=True,
                              verbose_name='Электронная почта',
                              help_text='Введите e-mail')
    first_name = models.CharField(max_length=constants.MAX_LENGTH_FIRST_NAME,
                                  verbose_name='Имя',
                                  help_text='Введите свое имя')
    last_name = models.CharField(max_length=constants.MAX_LENGTH_LAST_NAME,
                                 verbose_name='Фамилия',
                                 help_text='Введите свою фамилию')
    password = models.CharField(max_length=constants.MAX_LENGTH_PASSWORD,
                                verbose_name='Пароль для входа',
                                help_text='Придумайте пароль')
    username = models.CharField(
        max_length=constants.MAX_LENGTH_USERNAME, unique=True,
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
            models.CheckConstraint(
                name="Ограничение на самоподписку",
                check=~models.Q(user=models.F('author')),
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
