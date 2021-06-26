from django import forms
from django.contrib.auth.models import Group,Permission


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name','permissions')
        labels = {'name': 'İsim ', 'permissions': 'izinleri Seçiniz'}

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
            'permissions':forms.CheckboxSelectMultiple(),
        }