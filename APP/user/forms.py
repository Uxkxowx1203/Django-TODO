from django import forms
from django.contrib.auth.models import User
from .models import Todo


class myform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_pass = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        clean_data = super().clean()
        pwd = clean_data['password']
        cnfmpwd = clean_data['confirm_pass']
        if pwd != cnfmpwd:
            raise forms.ValidationError("Password does not match")
    class Meta():
        model = User
        fields =('first_name', 'last_name', 'username', 'email', 'password')

        
class TodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ['title', 'description', 'completed']
    widgets = {
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control'}),
    }