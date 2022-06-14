from django import forms
from account.models import Account
from product.models import Product
from .models import Supply
from account.forms import RegistrationForm


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
        
        widgets = {
            'label': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }

class SupplyForm(forms.ModelForm):
    label       = forms.CharField(label="Label", max_length=250, required=True, widget=forms.TextInput(
                    attrs={
                    'class':'form-control',
                    'placeholder':'Label'
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
        model = Supply
        fields = ['label', 'price', 'stock', 'description']


class SupplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['label', 'price', 'stock', 'description']
        
        widgets = {
            'label': forms.TextInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        }


class CreateAccountForm(RegistrationForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', "last_name", 'account_type']
        widgets = {
             'contact_number': forms.TextInput(attrs={'class':'form-control'}),
            'account_type': forms.Select(attrs={'class':'form-control'}, choices=[('admin', 'Admin'), ('customer', 'Customer'), ('farmer', 'Farmer'), ('staff', 'Staff')]),
        }


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', "last_name", 'address', 'contact_number', 'account_type']
        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'contact_number': forms.TextInput(attrs={'class':'form-control'}),
            'account_type': forms.Select(attrs={'class':'form-control'}, choices=[('admin', 'Admin'), ('customer', 'Customer'), ('farmer', 'Farmer'), ('staff', 'Staff')]),
        }
