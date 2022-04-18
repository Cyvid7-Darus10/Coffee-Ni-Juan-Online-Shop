from django import forms

class inventory_form(forms.Form):
    label       = forms.CharField(label="Label", max_length=250, required=True, widget=forms.TextInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Label'
                    }))
    image_url   = forms.CharField(label="Image URL", max_length=150, required=True, widget=forms.TextInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Image URL'
                    }))
    price       = forms.FloatField(label="Price", required=True, widget=forms.NumberInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Price'
                    }))
    stock       = forms.IntegerField(label="Stock", required=True, widget=forms.NumberInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Stock',
                    }))
    description = forms.CharField(label="Description", widget=forms.Textarea(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Description',
                    'rows':'3'
                    }))