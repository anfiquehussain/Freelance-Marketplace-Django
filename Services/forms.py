from django import forms
from .models import Overview, BasicPackage, StandardPackage, PremiumPackage, Description, Question, Gallery

class OverviewForm(forms.ModelForm):
    class Meta:
        model = Overview
        fields = ['titleOverview', 'category', 'search_tags']

class BasicPackageForm(forms.ModelForm):
    class Meta:
        model = BasicPackage
        fields = [
            'Basic_title', 'Basic_description', 'Basic_delivery_time',
            'Basic_revisions', 'Basic_source_file', 'Basic_price'
        ]

class StandardPackageForm(forms.ModelForm):
    class Meta:
        model = StandardPackage
        fields = [
            'Standard_title', 'Standard_description', 'Standard_delivery_time',
            'Standard_revisions', 'Standard_source_file', 'Standard_price'
        ]

class PremiumPackageForm(forms.ModelForm):
    class Meta:
        model = PremiumPackage
        fields = [
            'Premium_title', 'Premium_description', 'Premium_delivery_time',
            'Premium_revisions', 'Premium_source_file', 'Premium_price'
        ]

# class ExtraServiceForm(forms.ModelForm):
#     class Meta:
#         model = ExtraService
#         fields = ['title', 'pricing', 'delivery_time']


class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = ['description']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']



class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image1','image2','image3', 'video']
