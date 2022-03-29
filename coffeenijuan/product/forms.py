from django import forms

class productOrder(forms.Form):
	amount = forms.IntegerField(
		label = "", 
		widget = forms.TextInput(
			attrs = {'class':'amount col-2'}
			)
		)