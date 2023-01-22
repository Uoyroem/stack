from django import forms
from django.contrib.auth.forms import UserCreationForm
import re



phone_regexp = re.compile(r'(\+7|8) \d\d\d \d\d\d \d\d \d\d')


class SignupForm(UserCreationForm):
  phone_number = forms.CharField(max_length=20, empty_value='Введите номер телефона...', required=True,
                                 label='Номер телефона', help_text=f'Номер телефона должен соответсвовать паттерну: {phone_regexp.pattern}. Например: +7 484 283 98 98')
  
  def clean_phone_number(self):
    phone_number = self.cleaned_data['phone_number']
    if phone_regexp.match(phone_number) is None:
      raise forms.ValidationError(f'Номер телефона должен соответсвовать паттерну: {phone_regexp.pattern}')
    return phone_number
    