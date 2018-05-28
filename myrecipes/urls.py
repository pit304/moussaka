from django.urls import path

from . import views

app_name = 'myrecipes'
urlpatterns = [
    # ex: /
    path('', views.IndexView.as_view(), name='index'),
    # ex: /5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /5/vote/
    path('<int:recipe_id>/rate/', views.rate, name='rate'),
]
