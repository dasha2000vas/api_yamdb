from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Title(models.Model):
    title = models.CharField(max_length=256)


class Review(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = (-'pub_date',)


class Comment(models.Model):
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = (-'pub_date',)


TEXT_RESTRICTION = 256
SLUG_RESTRICTION = 50


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=TEXT_RESTRICTION,
    )
    slug = models.SlugField(
        max_length=SLUG_RESTRICTION,
        db_index=True,
        unique=True,
        verbose_name='Иденификатор',
    )

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры',
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=TEXT_RESTRICTION,
    )
    slug = models.SlugField(
        max_length=SLUG_RESTRICTION,
        db_index=True,
        unique=True,
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории',
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Произведение',
        max_length=TEXT_RESTRICTION,
    )
    year = models.IntegerField(
        verbose_name='Year of creation',
        validators=(validate_year,)
    )
    description = models.TextField(
        max_length=TEXT_RESTRICTION,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        null=True,
        on_delete=models.SET_NULL,
    )
    category = models.OneToOneField(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения',
        ordering = ('name',)

    def __str__(self):
        return self.name
