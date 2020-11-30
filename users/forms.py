"""
Contains form classes for User model.
"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs[
                "autofocus"
            ] = True

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


class UserChangeForm(BaseUserChangeForm):
    """
    A form for changing user information in admin interface.
    """

    class Meta:
        model = User
        fields = "__all__"
