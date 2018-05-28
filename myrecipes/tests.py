import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Recipe


class RecipeModelTests(TestCase):

    def test_was_published_recently_with_future_recipe(self):
        """
        was_published_recently() returns False for recipes whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_recipe = Recipe(pub_date=time)
        self.assertIs(future_recipe.was_published_recently(), False)


def test_was_published_recently_with_old_recipe(self):
    """
    was_published_recently() returns False for recipes whose pub_date
    is older than 1 day.
    """
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_recipe = Recipe(pub_date=time)
    self.assertIs(old_recipe.was_published_recently(), False)


def test_was_published_recently_with_recent_recipe(self):
    """
    was_published_recently() returns True for recipes whose pub_date
    is within the last day.
    """
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_recipe = Recipe(pub_date=time)
    self.assertIs(recent_recipe.was_published_recently(), True)


def create_recipe(title, days):
    """
    Create a recipe with the given `recipe_text` and published the
    given number of `days` offset to now (negative for recipes published
    in the past, positive for recipes that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Recipe.objects.create(title=title, pub_date=time)


class RecipeIndexViewTests(TestCase):
    def test_no_recipes(self):
        """
        If no recipes exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('myrecipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No recipes are available.")
        self.assertQuerysetEqual(response.context['latest_recipe_list'], [])

    def test_past_recipe(self):
        """
        Recipes with a pub_date in the past are displayed on the
        index page.
        """
        create_recipe(title="Past recipe.", days=-30)
        response = self.client.get(reverse('myrecipes:index'))
        self.assertQuerysetEqual(
            response.context['latest_recipe_list'],
            ['<Recipe: Past recipe.>']
        )

    def test_future_recipe(self):
        """
        recipes with a pub_date in the future aren't displayed on
        the index page.
        """
        create_recipe(title="Future recipe.", days=30)
        response = self.client.get(reverse('myrecipes:index'))
        self.assertContains(response, "No recipes are available.")
        self.assertQuerysetEqual(response.context['latest_recipe_list'], [])

    def test_future_recipe_and_past_recipe(self):
        """
        Even if both past and future recipes exist, only past recipes
        are displayed.
        """
        create_recipe(title="Past recipe.", days=-30)
        create_recipe(title="Future recipe.", days=30)
        response = self.client.get(reverse('myrecipes:index'))
        self.assertQuerysetEqual(
            response.context['latest_recipe_list'],
            ['<Recipe: Past recipe.>']
        )

    def test_two_past_recipes(self):
        """
        The recipes index page may display multiple recipes.
        """
        create_recipe(title="Past recipe 1.", days=-30)
        create_recipe(title="Past recipe 2.", days=-5)
        response = self.client.get(reverse('myrecipes:index'))
        self.assertQuerysetEqual(
            response.context['latest_recipe_list'],
            ['<Recipe: Past recipe 2.>', '<Recipe: Past recipe 1.>']
        )


class RecipeDetailViewTests(TestCase):
    def test_future_recipe(self):
        """
        The detail view of a recipe with a pub_date in the future
        returns a 404 not found.
        """
        future_recipe = create_recipe(title='Future recipe.', days=5)
        url = reverse('myrecipes:detail', args=(future_recipe.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_recipe(self):
        """
        The detail view of a recipe with a pub_date in the past
        displays the recipe's text.
        """
        past_recipe = create_recipe(title='Past recipe.', days=-5)
        url = reverse('myrecipes:detail', args=(past_recipe.id,))
        response = self.client.get(url)
        self.assertContains(response, past_recipe.title)
