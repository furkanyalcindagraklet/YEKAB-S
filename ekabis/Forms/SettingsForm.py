from django import forms

from ekabis.models.Settings import Settings


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('key', 'value')

        # labels = {'name': 'İsim '}
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control ', 'required': 'required'}),
        # }
