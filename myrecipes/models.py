import datetime

from django.db import models
from django.utils import timezone

class Recipe(models.Model):
    method_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
	
    def __str__(self):
        return self.method_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
	
    def __str__(self):
        return self.ingredient_text