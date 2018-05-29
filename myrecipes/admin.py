from django.contrib import admin

from .models import Recipe, Ingredient, Step


class StepInline(admin.TabularInline):
    model = Step
    extra = 3


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [StepInline, IngredientInline]
    list_display = ('title', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['title']


admin.site.register(Recipe, RecipeAdmin)
