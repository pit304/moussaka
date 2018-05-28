from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from myrecipes.forms import RatingForm
from .models import Recipe


class IndexView(generic.ListView):
    template_name = 'myrecipes/index.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        """
        Return the last five published recipes (not including those set to be
        published in the future).
        """
        return Recipe.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.edit.FormMixin, generic.DetailView):
    model = Recipe
    form_class = RatingForm
    template_name = 'myrecipes/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['rate'] = self.request.GET.get('rate')
        return context

    def get_queryset(self):
        """
        Excludes any recipes that aren't published yet.
        """
        return Recipe.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Recipe
    template_name = 'myrecipes/results.html'


def rate(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = RatingForm(request.POST)
    if form.is_valid():
        rating = form.save(commit=False)
        rating.date = timezone.now()
        rating.recipe = recipe
        rating.save()
        return HttpResponseRedirect(reverse('myrecipes:results', args=(recipe.id,)))
    else:
        return render(request, 'myrecipes/detail.html', {
            'recipe': recipe,
            'error_message': "You didn't add a rating.",
        })
