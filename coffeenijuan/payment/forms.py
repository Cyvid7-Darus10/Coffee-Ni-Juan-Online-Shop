from django import forms
from account.models import Account


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', "last_name", 'address', 'contact_number']
        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'contact_number': forms.TextInput(attrs={'class':'form-control'})
        }