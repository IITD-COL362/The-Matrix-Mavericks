from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(
        max_length=255,
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        )
    )

    address = forms.CharField(
        max_length=255,
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        )
    )

    city_id = forms.CharField(
        max_length=255,
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "City ID",
                "class": "form-control"
            }
        )
    )

    # mail_id = forms.CharField(
    #     max_length=255,
    #     label='',
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Mail ID",
    #             "class": "form-control"
    #         }
    #     )
    # )

    phone_number = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        )
    )

    birthday = forms.DateField(
        label='',
        required=False,
        widget=forms.DateInput(
            attrs={
                "placeholder": "Birthday",
                "class": "form-control",
                "type": "date"
            }
        )
    )

    sex = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        label='',
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )

    weight = forms.IntegerField(
        label='',
        required=False,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Weight",
                "class": "form-control"
            }
        )
    )

    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )

    username = forms.CharField(
        label='',
        max_length=20,
        min_length=4,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )

    password1 = forms.CharField(
        label='',
        max_length=30,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )

    password2 = forms.CharField(
        label='',
        max_length=30,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
