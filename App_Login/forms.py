from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile

class CreateNewUser(UserCreationForm):
    
    email = forms.EmailField(required=True, label = "", widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    username = forms.CharField(required=True, label = "", widget=forms.TextInput(attrs={'placeholder': 'Your Username'}))
    password1 = forms.CharField(required=True, label="",widget= forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(required=True, label="",widget= forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class EditProfile(forms.ModelForm):
    sex = forms.ChoiceField(
        choices=UserProfile.SEX_CHOICES,
        widget=forms.Select(attrs={
            'style': 'font-size: 19px; height: 25px;',  
        }),
        required=False
    )
    
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))


    
    class Meta:
        model = UserProfile
        exclude = ('user',)

from django import forms
from core.models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'price', 'duration_days']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
