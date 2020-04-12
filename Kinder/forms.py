from django import forms
from .models import Kinder


class KinderForm(forms.ModelForm):
    class Meta:
        model = Kinder
        fields = '__all__'

