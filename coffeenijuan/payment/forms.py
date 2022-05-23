from django import forms

class OrderForm(forms.Form):
	address = forms.CharField(
		label = "", 
		widget = forms.TextInput(
			attrs = {	'name':'address',
						'placeholder':'Address',
						'maxlength':'60', 
						'autofocus':'true',
						'required':'true',
						'id':'id_address'
					}
			)
		)