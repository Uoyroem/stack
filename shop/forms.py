from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class ReviewForm(forms.ModelForm):
  class Meta:
    model = models.Review
    fields = ['rating', 'review_text']
    labels = {
      'review_text': _('Отзыв')
    }
