from django import forms
from .models import GSTDeclaration
import re
from django.core.files.base import ContentFile


class GSTForm(forms.ModelForm):
    turnover = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')], widget=forms.RadioSelect)

    # Required Images
    customer_photo = forms.ImageField(required=True)
    gst_certification_photo = forms.ImageField(required=True)
    udyan_adhar_photo = forms.ImageField(required=True)
    personal_pan_photo = forms.ImageField(required=True)
    personal_adhar_photo = forms.ImageField(required=True)
    drug_license_photo20b = forms.ImageField(required=False)
    drug_license_photo21b = forms.ImageField(required=False)
    drug_license_photo20d = forms.ImageField(required=False)
    food_license_photo = forms.ImageField(required=False)
    shop_photo = forms.ImageField(required=True)

    class Meta:
        model = GSTDeclaration
        exclude = ['tds_tcs']  # Exclude tds_tcs from the form
        widgets = {
            'gst_number': forms.TextInput(attrs={'placeholder': 'Enter GST Number', 'class': 'form-control'}),
            'year_of_filing': forms.TextInput(attrs={'placeholder': 'Enter year of filing', 'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Enter Company Name', 'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'placeholder': 'Enter Company Address', 'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City', 'class': 'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'Enter State', 'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'placeholder': 'Enter Pincode', 'class': 'form-control', 'maxlength': 6}),
            'office_mobile_number': forms.TextInput(attrs={'placeholder': 'Enter Office Mobile Number', 'class': 'form-control'}),
            'personal_mobile_number': forms.TextInput(attrs={'placeholder': 'Enter Personal Mobile Number', 'class': 'form-control'}),
            'company_email_address': forms.EmailInput(attrs={
            'placeholder': 'Enter Company Email Address',
            'class': 'form-control'}),
            'pan_number': forms.TextInput(attrs={'placeholder': 'Enter PAN Number', 'class': 'form-control'}),
            'tan_number': forms.TextInput(attrs={'placeholder': 'Enter TAN Number', 'class': 'form-control'}),
            'drug_license_validity20b': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'drug_license_validity21b': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'drug_license_validity20d': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if not re.match(r'^[0-9A-Z]{15}$', gst_number):
            raise forms.ValidationError("Invalid GST Number format. It should be 15 characters long.")
        return gst_number

    def clean_pan_number(self):
        pan_number = self.cleaned_data.get('pan_number')
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_number):
            raise forms.ValidationError("Invalid PAN Number format. Example: ABCDE1234F")
        return pan_number

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if not re.match(r'^[A-Za-z0-9\s&.\'-]{2,100}$', company_name):
            raise forms.ValidationError("Invalid company name format. Use letters, numbers, and basic punctuation.")
        return company_name

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if not re.match(r'^\d{6}$', pincode):
            raise forms.ValidationError("Invalid Pincode. It should be 6 digits long.")
        return pincode

    def clean_tan_number(self):
        tan_number = self.cleaned_data.get('tan_number')
        if tan_number and not re.match(r'^[A-Z]{4}[0-9]{5}[A-Z]$', tan_number):
            raise forms.ValidationError("Invalid TAN Number format. Example: ABCD12345E")
        return tan_number
    
    def clean_turnover(self):
        turnover = self.cleaned_data.get('turnover')
        if turnover not in ['yes', 'no']:
            raise forms.ValidationError("Please select a valid turnover option.")
        return turnover

    def clean_office_mobile_number(self):
        number = self.cleaned_data.get('office_mobile_number')
        if not re.match(r'^\d{10}$', number):
            raise forms.ValidationError("Invalid Office Mobile Number. It should be 10 digits.")
        return number

    def clean_personal_mobile_number(self):
        number = self.cleaned_data.get('personal_mobile_number')
        if not re.match(r'^\d{10}$', number):
            raise forms.ValidationError("Invalid Personal Mobile Number. It should be 10 digits.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        for field_name in [
            'customer_photo', 'gst_certification_photo', 'udyan_adhar_photo', 'personal_pan_photo',
            'personal_adhar_photo', 'drug_license_photo20b', 'drug_license_photo21b',
            'drug_license_photo20d', 'food_license_photo', 'shop_photo'
        ]:
            file = cleaned_data.get(field_name)
            if file and not file.content_type.startswith('image'):
                self.add_error(field_name, "Invalid file format. Upload an image.")