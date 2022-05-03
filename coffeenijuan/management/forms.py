from django import forms
from product.models import Product

class InventoryForm(forms.ModelForm):
    label       = forms.CharField(label="Label", max_length=250, required=True, widget=forms.TextInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Label'
                    }))
    image       = forms.ImageField(label="Image", required=True, widget=forms.FileInput(
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

    class Meta:
        model = Product
        fields = ['label', 'image', 'price', 'stock', 'description']


class InventoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['label', 'image', 'price', 'stock', 'description']
        
        # add class name for bootstrap
        widgets = {
            'label': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }
