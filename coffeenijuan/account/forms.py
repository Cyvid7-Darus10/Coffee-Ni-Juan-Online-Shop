from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, widget=forms.EmailInput(
            attrs={'placeholder': 'Email', 'class': 'form-control'}
            ), help_text='Valid Email Required'
        )
    username = forms.CharField(
        max_length=60, widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'form-control'}
            )
        )
    first_name = forms.CharField(
        max_length=60, widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'form-control'}
                )
            )
    last_name = forms.CharField(
        max_length=60, widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'form-control'}
            )
        )
    password1 = forms.CharField(
        max_length=60, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control'}
            )
        )
    password2 = forms.CharField(
        max_length=60, widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}
            )
        )
    
    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', "last_name", 'password1', 'password2')
        
   
    def __init__(self, *args, **kwargs): 
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['email'].label = ''
        self.fields['username'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
    
        
class AccountAuthenticationForm(forms.ModelForm):
	password = forms.CharField(
        label='Password', widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
            )
        )

	class Meta:
		model = Account
		fields = ('email', 'password')
		widgets = {
        	'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
    	}

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class ForgotPassword(forms.Form):
    email = forms.EmailField(
        max_length=60, widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}
            ), help_text='Valid Email Required'
        )

