from django import forms
from .models import RetailRow


class CSVUploadForm(forms.Form):
    file = forms.FileField()


class RetailRowAnnotateForm(forms.ModelForm):
    class Meta:
        model = RetailRow
        fields = ["retailer", "segment"]
        widgets = {
            "retailer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter retailer name",
                }
            ),
            "segment": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
