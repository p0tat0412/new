from django.forms import ModelForm
from .models import *

class company_form(ModelForm):
    class Meta:
        model = company
        fields = '__all__'

class contact_form(ModelForm):
    class Meta:
        model = contact_info
        fields = '__all__'

