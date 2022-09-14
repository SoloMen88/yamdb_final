from datetime import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

USER_ROLE_USER = 'user'
USER_ROLE_ADMIN = 'admin'
USER_ROLE_MODERATOR = 'moderator'


class User(AbstractUser):
    """Кастомный класс пользователя Django"""

    UserRoleChoices = (
        (USER_ROLE_USER, 'Пользователь'),
        (USER_ROLE_ADMIN, 'Администратор'),
        (USER_ROLE_MODERATOR, 'Модератор')
    )

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=60, unique=True)
    role = models.CharField('права доступа', max_length=16,
                            choices=UserRoleChoices, default=USER_ROLE_USER)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=20, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    @property
    def is_admin(self):
        if self.role == USER_ROLE_ADMIN or self.is_superuser:
            return True

    @property
    def is_moderator(self):
        return self.role == USER_ROLE_MODERATOR or self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('username',)


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('pk',)


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Произведение')
    year = models.IntegerField(
        validators=[MaxValueValidator(dt.now().year)],
        verbose_name='Дата выхода'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genres,
        through='GenresTitles',
        related_name='genre',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='category',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class GenresTitles(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField(
        'Текст',
        help_text='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        help_text='Дата отзыва',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='review'
    )
    score = models.SmallIntegerField(
        'Счёт',
        validators=[
            MaxValueValidator(10,
                              'Максимальная оценка не может быть больше 10'),
            MinValueValidator(1,
                              'Минимальная оценка не может быть меньше 1')
        ]
    )
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'], name='unique_title_author')
        ]
        ordering = ('pk',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        'Комментарий',
        help_text='Текст комментария',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        help_text='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв с комментарием',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pk',)

    def __str__(self):
        return self.text
