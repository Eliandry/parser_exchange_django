from django import forms
class UserForm(forms.Form):
    email=forms.EmailField(required=True)
    diff=forms.IntegerField(required=True,min_value=1,max_value=10)
