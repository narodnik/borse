from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    password_again = forms.CharField()

class OrderForm(forms.Form):
    price = forms.DecimalField()
    amount = forms.DecimalField()
    order_type = forms.ChoiceField(choices=(('Buy', 'Buy'), ('Sell', 'Sell')),
                                   widget=forms.RadioSelect)

