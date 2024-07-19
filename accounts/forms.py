from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User,EmployeeEmployer, JobSeeker,Address,Message
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.utils import timezone
from django.forms import (
    ModelForm,
    TextInput,
    PasswordInput,
    CharField,
    CheckboxInput,
    DateField,
    DateInput,
    Select,
    Form
)

class LoginForm(AuthenticationForm):
    username = CharField(
        max_length = 15,
        min_length = 4,
        label = 'Username',
        required = True,
        widget = TextInput({
                'class': 'form-control'
            })
    )

    password = CharField(
        max_length = 25,
        min_length = 4,
        label = 'Password',
        required = True,
        widget = PasswordInput({
                'class': 'form-control'
            })
    )



class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=("First Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label=("Last Name"),
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        min_length=5,
        max_length=50,
        label="Email",
        required=True,
        validators=[EmailValidator()],
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class EmployeeEmployerForm(ModelForm):
    designation = CharField(
        label=("Designation"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    location = CharField(
        label=("First Name"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    company_name = CharField(
        label=("First Name"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )




    class Meta:
        model = EmployeeEmployer
        fields = [
            "designation",
            "location",
            "company_name",
            
        ]
        

class ProfileForm(forms.ModelForm):
    dob = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={"class": "form-control"}),
        initial=timezone.now,
    )
    gender = forms.CharField(
        label="Gender",
        required=False,
        widget=forms.Select(
            choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
            attrs={"class": "form-select"},
        ),
    )
    phone = forms.CharField(
        label="Phone",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    qualification = forms.CharField(
        label="Qualification",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    bio =forms.CharField(
        label="Bio",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )
    smoke = forms.CharField(
        label="Smoke",
        required=False,
        widget=forms.Select(
            choices=[("N", "Non-Smoker"), ("O", "Occasional Smoker"), ("R", "Regular Smoker")],
            attrs={"class": "form-select"},
        ),
    )
    drinking = forms.CharField(
        label="Drinking",
        required=False,
        widget=forms.Select(
            choices=[("N", "Non-Drinker"), ("O", "Occasional Drinker"), ("R", "Regular Drinker")],
            attrs={"class": "form-select"},
        ),
    )
    rel_status = forms.CharField(
        label="Relationship Status",
        required=False,
        widget=forms.Select(
            choices=[
                ("S", "Single"),
                ("M", "Married"),
                ("W", "Widow"),
                ("D", "Divorced"),
            ],
            attrs={"class": "form-select"},
        ),
    )
    profile_pic = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control '})
    )
    short_reel = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control '})
    )

    class Meta:
        model = User
        fields = [
            "dob",
            "gender",
            "phone",
            "bio",
            "qualification",
            "smoke",
            "drinking",
            "rel_status",
            "profile_pic",
            "short_reel",
        ]

class JobSeekerForm(ModelForm):
    job_field = CharField(
        label=("Job Field"),
        max_length=30,
        required=False,
        widget=TextInput(attrs={"class": "form-control"}),
    )
    experience = CharField(
        label="Experience",
        required=False,
        widget=Select(
            choices=[("B", "Beginner"), ("I", "Intermediate"), ("E", "Expert")],
            attrs={"class": "form-select"},
        ),
    )

    class Meta:
        model = JobSeeker
        fields = [
            "job_field",
            "experience"
        ]




class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'city', 'district', 'state', 'pincode', 'country']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']