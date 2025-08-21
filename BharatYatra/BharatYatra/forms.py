from django import forms
from registration_data.models import CustomUser
from django.core.validators import RegexValidator
from contact.models import ContactData
from profileapp.models import User_Profile

class loginForm(forms.Form):
    username= forms.CharField(max_length=100, validators=
                              [RegexValidator(regex=r'^[A-za-z0-9_]+$',
                                              message="Username can only contain letters, numbers, and underscores.",
                                              code="Invalid Username")], 
                                              widget=forms.TextInput,
                                              label="Username")
    password= forms.CharField(widget=forms.PasswordInput, label="Password")
    remember_me = forms.BooleanField(required=False, label="Remember Me")

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['fullname', 'email', 'password', 'gender', 'username', 'phone']
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

class ContactDetails(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=10, required=True, validators=[
                            RegexValidator(r'^\d{10}$')])
    email = forms.CharField(max_length=254, required=True)
    message = forms.CharField(max_length=500, required=True)

class FormProfile(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ['user', 'profile_img', 'bio', 'contact', 'trip_organised', 'places_visited']


