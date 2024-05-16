from django import forms
from seller.models import product_seller
from .models import *

class MyProductForm(forms.ModelForm):
    class Meta:
        model = product_seller
        fields = '__all__'


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()


class EmailForm(forms.ModelForm):
    class Meta:
        model = emailSetting
        fields = "__all__"