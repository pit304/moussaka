import datetime

from django.db import models
from django.utils import timezone


STAR_CHOICES = (
    (5, '*****'),
    (4, '****'),
    (3, '***'),
    (2, '**'),
    (1, '*'),
)


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.step_text


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.ingredient_text


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    stars = models.IntegerField(choices=STAR_CHOICES, default=5)
    comment = models.CharField(max_length=200, default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ": " + str(self.stars) + " stars"
