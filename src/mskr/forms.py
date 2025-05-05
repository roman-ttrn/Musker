from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Meep, Profile

class MeepForm(forms.ModelForm):
    body = forms.CharField(widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Body of your Meep",
            "class": "form-control"
        }
    ), 
    label="",
    )

    class Meta:
        model = Meep
        exclude = ("user", "created", 'likes')

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # copying behavior of parent class


        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'ttrn1@gmail.com'
        self.fields['email'].label = 'Email adress'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'


        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.' \
        '</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.' \
        '</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class ProfPicForm(forms.ModelForm):
    prof_image = forms.ImageField(label="Profile Picture")
    class Meta:
        model = Profile
        fields = ('prof_image', )


class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }),
        required=True
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }),
        required=False
    )
    new_password2 = forms.CharField(
        label="Confirm Your New Passwod",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }),
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        user = self.instance  # Текущий пользователь
        current_password = cleaned_data.get('current_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # Проверяем, ввел ли пользователь верный текущий пароль
        if not authenticate(username=user.username, password=current_password):
            raise forms.ValidationError("It's wrong password")

        # Если введен новый пароль, проверяем совпадение
        if new_password1 or new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("New password doesn't match with confomative password!")
        if new_password1 and new_password2:
            try:
                validate_password(new_password1)
            except ValidationError as e:
                self.add_error('new_password1', e)

        return cleaned_data
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password1')

        if new_password:
            user.set_password(new_password)  # Меняем пароль

        if commit:
            user.save()

        return user
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # copying behavior of parent class


        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'ttrn1@gmail.com'
        self.fields['email'].label = 'Email adress'

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'


        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

