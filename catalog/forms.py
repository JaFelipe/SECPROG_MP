from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from catalog.choices import *


QUESTIONS_CHOICES = (('pet','Whats the name of your first pet?'),
                ('superhero','Who is your childhood superhero?'),
                ('maiden','What is your mother\'s maiden name?'),
                ('teacher','Who is your favorite teacher?'))

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True )
    middle_name = forms.CharField(max_length=30, required=True )
    last_name = forms.CharField(max_length=30, required=True )
    username = forms.CharField(max_length=30, required=True) 
    email = forms.EmailField(max_length=254, required=True)
    birth_date = forms.DateField(required=True,help_text=' YYYY-MM-DD')
    studentNum = forms.IntegerField(required=True,label="ID Number: ", help_text='11539267')
    favorite_fruit = forms.CharField(max_length=6,label="Secret Questions", initial='', widget=forms.Select(choices=QUESTIONS_CHOICES), required=True)
    secretAnswer = forms.CharField(max_length=254,label="Answer",required=True)
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
    
    def save(self, commit=True):
        User = super(RegistrationForm, self).save(commit=False)

        
        if commit:
            User.save()
            
        return User
    