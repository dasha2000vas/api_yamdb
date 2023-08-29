from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=256)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    score = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
