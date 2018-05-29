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
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step_text = models.TextField(max_length=1000)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.step_text


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_text = models.CharField(max_length=300)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.ingredient_text


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    stars = models.IntegerField(choices=STAR_CHOICES, default=5)
    comment = models.TextField(max_length=1000, default=None, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + ": " + str(self.stars) + " stars"
