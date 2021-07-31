from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Message", min_length=20)
