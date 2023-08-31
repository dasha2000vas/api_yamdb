from django.db import models

from .validators import validate_year

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
