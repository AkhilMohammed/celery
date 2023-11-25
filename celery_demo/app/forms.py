from django import forms

class RegistrationForm(forms.Form):
    userName = forms.CharField()
    email = forms.EmailField()
    firstName = forms.CharField()
    lastName = forms.CharField()
    password = forms.CharField()
    userType = forms.CharField()


class loginForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class otpForm(forms.Form):
    otp = forms.CharField(max_length=6)