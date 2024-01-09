from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Match, Submissions


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("username","email","password1","password2")

    def __init__(self,*args,**kwargs):
        super(RegisterUserForm,self).__init__(*args,**kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'

class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ('match_id','match_date','match_start_time','match_team_A','match_team_B','match_status','match_winner')
        labels = {
            'match_id' : '',
            'match_date': '',
            'match_start_time': '',
            'match_team_A': '',
            'match_team_B': '',
            'match_status': '',
            'match_winner': '',
        }

        widgets = {
            'match_id' : forms.TextInput(attrs={'class':'form-control','placeholder':'Match ID'}),
            'match_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Match Date'}),
            'match_start_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Match Start Time'}),
            'match_team_A': forms.TextInput(attrs={'class':'form-control','placeholder':'Match Team A'}),
            'match_team_B': forms.TextInput(attrs={'class':'form-control','placeholder':'Match Team B'}),
            'match_status': forms.TextInput(attrs={'class':'form-control','placeholder':'Match Status'}),
            'match_winner': forms.TextInput(attrs={'class':'form-control','placeholder':'Match Winner'}),
        }
