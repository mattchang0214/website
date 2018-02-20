from accounts.models import UserProfile
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, PasswordResetForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'email',
        ]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = [
            'user',
            'total',
        ]
        labels = {
            'tufts_id': 'Tufts ID',
            'phone': 'Phone (Optional)',
        }

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]

# Source: https://stackoverflow.com/questions/27734185/inform-user-that-email-is-invalid-using-djangos-password-reset
class EmailValidation(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")

        return email