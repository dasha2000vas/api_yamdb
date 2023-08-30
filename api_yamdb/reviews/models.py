from django.db import models

from . import constants
from .validators import validate_year


class Genre(models.Model):
    name = models.CharField(
        max_length=constants.TEXT_RESTRICTION,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        max_length=constants.SLUG_RESTRICTION,
        db_index=True,
        unique=True,
        verbose_name='Иденификатор',
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=constants.TEXT_RESTRICTION,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=constants.SLUG_RESTRICTION,
        db_index=True,
        unique=True,
        verbose_name='Идентификатор',
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=constants.TEXT_RESTRICTION,
        verbose_name='Произведение'
    )
    year = models.IntegerField(
        verbose_name='Year of creation',
        validators=(validate_year,)
    )
    description = models.TextField(
        max_length=constants.TEXT_RESTRICTION,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name
