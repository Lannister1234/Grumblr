from django import forms
from django.contrib.auth.models import User
from grumblr.models import *


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']
    password2 = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        first_name = cleaned_data.get('first_name')
        if ' ' in first_name:
            raise forms.ValidationError("Space is not allowed in first name.")

        last_name = cleaned_data.get('last_name')
        if ' ' in last_name:
            raise forms.ValidationError("space is not allowed in last name.")

        email = cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("This email is already taken.")

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and len(password) < 5:
            raise forms.ValidationError("Password length should exceed 5 characters!")
        if password != password2:
            raise forms.ValidationError("Two input passwords do not match!")
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', ]

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        text = cleaned_data.get('text')

        if not text or text == '':
            raise forms.ValidationError("Post text is not in correct format.")
        if len(text) > 42:
            raise forms.ValidationError("Posted text should not exceed 42 characters.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'first_name', 'last_name', 'bio', 'photo']
        widgets = {'photo': forms.FileInput()}

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        return cleaned_data


class ResetPwdForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password',]
    password2 = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(ResetPwdForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and len(password) < 5:
            raise forms.ValidationError("Password length should exceed 5 characters!")
        if password != password2:
            print(password)
            print(password2)
            raise forms.ValidationError("Two input passwords do not match!")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        text = cleaned_data.get('text')
        if not text or text == '':
            raise forms.ValidationError("Comment text is not in correct format.")
        if len(text) > 42:
            raise forms.ValidationError("Comment text should not exceed 42 characters.")
        return cleaned_data