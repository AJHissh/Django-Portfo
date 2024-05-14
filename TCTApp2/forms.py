from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm  


class CategorytwoForm(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categorytwo
        exclude = ['user', 'date_opened', 'date_submitted', 'task_company','is_completed','month_submit', 'date_today']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
            'question_1': forms.Select,
            'question_4': forms.Select
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.username
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
        self.fields['elapsed_time'].initial = elapsed_time
        
        
class CategorytwoForm2(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categorytwo2  
        exclude = ['user', 'date_opened', 'date_submitted', 'task_company','is_completed','month_submit', 'date_today']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        email = kwargs.pop('email', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.username
            print(f'Email parameter: {email}')
            self.fields['email'].initial = email
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
        self.fields['elapsed_time'].initial = elapsed_time
        
class CategorytwoForm3(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categorytwo3  
        exclude = ['user', 'date_opened', 'date_submitted', 'task_company','is_completed','month_submit', 'date_today']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        email = kwargs.pop('email', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = user.username
            print(f'Email parameter: {email}')
            self.fields['email'].initial = email
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
        self.fields['elapsed_time'].initial = elapsed_time
        