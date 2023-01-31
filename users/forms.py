from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from utils.classes_adder import classes_adder
import re



class LoginForm(AuthenticationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs);
    classes_adder(self, 'input');


phone_regexp = re.compile(r'(\+7|8) \d\d\d \d\d\d \d\d \d\d')


class SignupForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    classes_adder(self, 'input')
    
  phone_number = forms.CharField(max_length=20, empty_value='Введите номер телефона...', required=True,
                                 label='Номер телефона', help_text=f'Номер телефона должен соответсвовать паттерну: {phone_regexp.pattern}. Например: +7 484 283 98 98')
  email = forms.EmailField()
  
  def clean_phone_number(self):
    phone_number = self.cleaned_data['phone_number']
    if phone_regexp.match(phone_number) is None:
      raise forms.ValidationError(f'Номер телефона должен соответсвовать паттерну: {phone_regexp.pattern}')
    return phone_number
  
  def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    