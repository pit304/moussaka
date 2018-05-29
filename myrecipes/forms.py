from django import forms
# from django.forms import Textarea

from .models import Rating


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('user', 'stars', 'comment',)
#        widgets = {
#            'comment': Textarea(attrs={'cols': 40, 'rows': 10}),
#        }
