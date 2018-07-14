from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=4)
    password = forms.CharField(max_length=16, min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=4)
    password = forms.CharField(max_length=16, min_length=6)
    remember = forms.BooleanField()
