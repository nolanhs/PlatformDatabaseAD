from django import forms
from .models import Application, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'cover_letter', 'attachment']
        
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False)
    organization = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "full_name", "phone_number", "age", "organization")

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            profile = user.profile
            profile.full_name = self.cleaned_data["full_name"]
            profile.email = self.cleaned_data["email"]
            profile.phone_number = self.cleaned_data.get("phone_number")
            profile.age = self.cleaned_data.get("age")
            profile.organization = self.cleaned_data.get("organization")
            profile.save()
        return user