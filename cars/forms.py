from django import forms
from .models import Parking

class ParkingsForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = [
            'reg_number',
            'colour',
            ]
        
class ParkingsForm1(forms.ModelForm):
    class Meta:
        model = Parking
        fields = [
            'colour',
            ]