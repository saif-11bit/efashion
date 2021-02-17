from django import forms

class CheckoutForm(forms.Form):
	street_address = forms.CharField(required=False)
	address_line2 = forms.CharField(required=False)
	state = forms.CharField(required=False)
	city = forms.CharField(required=False)
	pin_code = forms.CharField(required=False,max_length=6)
	set_default_address = forms.BooleanField(required=False)
	use_default_address = forms.BooleanField(required=False)
	# payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_METHOD)


class CouponForm(forms.Form):
	code = forms.CharField(label='',widget=forms.TextInput(attrs={
		'class': 'form-control',
		'placeholder': 'Promo code',
		'aria-label':"Recipient's username",
		'aria-describedby':"basic-addon2"
	}))
