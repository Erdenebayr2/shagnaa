from django import forms
from .models import *
class DriverForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['phone_number', 'date_of_passport', 'licenseid', 'passport_image']

    def __init__(self, *args, **kwargs):
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['date_of_passport'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['passport_image'].widget = forms.FileInput()

class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = ['register', 'vehicletype', 'edangi', 'trademark_or_manufacturer', 'certificate_number']

class TrailerFileForm(forms.ModelForm):
    class Meta:
        model = TrailerFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(TrailerFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget = forms.FileInput()

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['product', 'driver', 'trailer', 'issuccess']
