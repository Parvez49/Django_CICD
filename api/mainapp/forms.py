from typing import Any
from django import forms
from .models import Post, Profile, Comment, UserPreference
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Profile extras form
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Picture")
    profile_bio = forms.CharField(label="Profile Bio", max_length=500, widget=forms.Textarea(attrs={'class':'form-control', "placeholder": "Discribe yourself"}))
    facebook_link = forms.CharField(label="Facebook Link", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "Your facebook profile link"}))
    linked_link = forms.CharField(label="LinkedIn Link", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "Your facebook profile link"}))
    instagram_link = forms.CharField(label="Instagram Link", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "Your facebook profile link"}))

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'facebook_link', 'linked_link', 'instagram_link')
# newpost
class PostForm(forms.ModelForm):
    post_image = forms.ImageField(label="Post Picture", required=False)
    body = forms.CharField(required=True, 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Write your post here",
                                   "class": "form-control h-25 text-black w-100",
                                }
                            ),
                           label="",
                           )
    class Meta:
        model = Post
        fields = ('body','post_image')
        exclude = ("user", "likes", "loves")


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control   rounded-pill py-2', 'placeholder':'Email address'}))
    first_name = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control rounded-pill py-2', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control rounded-pill py-2', 'placeholder':'Last name '}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control rounded-pill py-2'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-white"><small>Required</small>'

        self.fields['password1'].widget.attrs['class'] = 'form-control rounded-pill py-2'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-white"><small>Password can not be too small or commonly used password</small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control rounded-pill py-2'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-white"><small>Enter the same password as before</small>'


# For update
class ProfileUpdateForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address'}))
    first_name = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=200, label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class="form-text text-white"><small>Password can not be too small</small>'

        self.fields['password2'].widget.attrs['class'] = 'form-control text-white'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before</small>'

# Comments for specific post
class CommentForm(forms.ModelForm):
    comment_image = forms.ImageField(label="", required=False, widget=forms.widgets.FileInput(
        attrs={
            "class":""
        }
    ))
   
    body = forms.CharField(required=True, 
                           widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Write your comment here",
                                   "class": "form-control text-black",
                                   "rows": 1,
                                }
                            ),
                           label="",
                           )
    class Meta:
        model = Comment
        fields = ( 'body','comment_image',)
        exclude = ("user", "post")

# User preference update form
class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ('user', 'preference')
