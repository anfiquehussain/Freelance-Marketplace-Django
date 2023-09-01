from django import forms
from .models import UserProfile, Certification, Language

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'country', 'state', 'website_link', 'about_me', 'skills']
        widgets = {
            'skills': forms.CheckboxSelectMultiple,
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['title', 'issuing_organization', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language', 'proficiency']
