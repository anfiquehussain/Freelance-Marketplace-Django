# forms.py

from django import forms
from .models import Order_Requirements

class OrderRequirementsForm(forms.ModelForm):
    class Meta:
        model = Order_Requirements
        fields = ['description', 'answer_1', 'example_image']  # Define the fields you want to include in the form
