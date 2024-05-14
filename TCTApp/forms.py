from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


##----------------------------------------------##

## Form creation for App 1 Forms ##

##----------------------------------------------##
  
  
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        # Update widget attributes and placeholders for each field
        self.fields['username'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control reg', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # # Check if the email ends with '@gmail.com'
        # if not email.endswith('@gmail.com'):
        #     raise ValidationError('Please enter a valid gmail email address')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
    
    
class RequestEditForm(forms.ModelForm):
    class Meta:
        model = RequestEdit
        exclude = ['user', 'status', 'id']
        widgets = {
            'record_ID': forms.TextInput(attrs={'readonly': True}),
            'name': forms.TextInput(attrs={'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Set up form helper and add a submit button
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit', style='background-color: #9CCBFD; color: #0c077d;'))

        # Set initial value for the 'name' field based on the user's first and last name
        if user:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"


    

# Create form for the NoioreTask Model
class CategoryoneForm(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categoryone
        exclude = ['user', 'date_opened', 'date_today', 'month_submit', 'date_submitted', 'task_company', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'question_3': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)

        # Set initial values for the 'name' and 'elapsed_time' fields
        if user:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
       
        
        

class CategoryoneForm2(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categoryone2
        exclude = ['user', 'date_opened','date_today', 'month_submit', 'date_submitted', 'task_company', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'question_1': forms.Select,
            'question_5': forms.Select,
            'question_8': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
        self.fields['elapsed_time'].initial = elapsed_time
        
        
class CategoryoneForm3(forms.ModelForm):
    elapsed_time = forms.DurationField(widget=forms.HiddenInput())

    class Meta:
        model = Categoryone3
        exclude = ['user', 'date_opened','date_today', 'month_submit', 'date_submitted', 'task_company', 'is_completed']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'task_segment': forms.TextInput(attrs={'readonly': True}),
            'client': forms.TextInput(attrs={'readonly': True}),
            'question_3': forms.Select,
            'question_4': forms.Select,
            'question_12': forms.Select,
            'question_13': forms.Select,
            'question_14': forms.Select,
            'question_15': forms.Select,
            'question_16': forms.Select,
            'question_17': forms.Select,
            'question_18': forms.Select,
            'question_19': forms.Select,
            'question_20': forms.Select,
            'question_21': forms.Select,
            'question_24': forms.Select,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        elapsed_time = kwargs.pop('elapsed_time', 0)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['name'].initial = f"{user.first_name} {user.last_name}"
        self.fields['elapsed_time'].initial = elapsed_time

    def update_elapsed_time(self, elapsed_time):
        self.cleaned_data['elapsed_time'] = elapsed_time
        self.fields['elapsed_time'].initial = elapsed_time


##----------------------------------------------##

## END Form creation for App 1 Forms ##

##----------------------------------------------##



