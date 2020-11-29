"""
Contains form classes for User model.
"""
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Form class for creating a user.
    """

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "password",
        )

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
