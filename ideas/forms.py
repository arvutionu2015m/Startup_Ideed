# ideas/forms.py
from django import forms
from .models import StartupIdea

class StartupIdeaForm(forms.ModelForm):
    class Meta:
        model = StartupIdea
        fields = ['description', 'image']
