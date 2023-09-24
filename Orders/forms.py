# forms.py

from django import forms
from .models import Order_Requirements
from .models import DeliveryDetails


class OrderRequirementsForm(forms.ModelForm):
    class Meta:
        model = Order_Requirements
        fields = ['description', 'answer_1', 'example_image']  # Define the fields you want to include in the form


class DeliveryDetailsForm(forms.ModelForm):
    class Meta:
        model = DeliveryDetails
        fields = ['delivery_notes','delivery_file']

