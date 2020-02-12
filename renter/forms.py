from django import forms
from django.contrib.auth.models import User
from .models import *


class UserForm(forms.ModelForm):
    first_name= forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'class':'input--style-3','placeholder':"First name"}))
    last_name= forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'class':'input--style-3','placeholder':"Last name"}))
    username= forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'class':'input--style-3','placeholder':"Username"}))
    password= forms.CharField(max_length=100,widget= forms.PasswordInput
                           (attrs={'class':'input--style-3','placeholder':"Password"}))
    email= forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'class':'input--style-3','placeholder':"Email"}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name','username','password','email')



class UserProfileInfoForm(forms.ModelForm):
    birth_date= forms.DateField(widget= forms.TextInput
                           (attrs={'class':"input--style-3 js-datepicker",'placeholder':"Birthdate"}))
    phone= forms.CharField(max_length=100,widget= forms.TextInput
                           (attrs={'class':'input--style-3','placeholder':"Phone"}))
    class Meta:
        model = Profile
        fields = ('birth_date','phone','gender','profile_pic','role')



class PropertyUpdateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('user', 'title', 'property_pic' ,'description' ,'address', 'price' ,'sqft')