from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django import forms
import pytz
from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from django import forms
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.urls import path


##----------------------------------------------##

## Django Admin View ##

##----------------------------------------------##

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Optionally, customize the list_display, list_filter, search_fields, etc.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')

User = get_user_model()
    
class RequestEditAdminForm(forms.ModelForm):
    class Meta:
        model = RequestEdit
        fields = ['id', 'name', 'record_ID', 'change', 'reason', 'status']
        
class RequestEditAdmin(admin.ModelAdmin):
    form = RequestEditAdminForm
    list_display = ('id','name', 'record_ID', 'change', 'status')
    
class CategoryoneAdminForm(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categoryone
        fields = ['name', 'task_company','client','date_today','month_submit','task_segment', 'date_opened', 'date_submitted','is_completed', 'company', 'question_1', 'question_2', 'question_3']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }

class CategoryoneAdmin(SimpleHistoryAdmin):
    form = CategoryoneAdminForm
    list_display = ('id', 'name', 'elapsed_time', 'time_date_opened', 'time_date_submitted', 'is_completed')
    
    def time_date_opened(self, obj):
        if obj.date_opened is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_opened.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''

    def time_date_submitted(self, obj):
        if obj.date_submitted is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_submitted.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''
    
    time_date_opened.admin_order_field = 'date_opened'
    time_date_opened.short_description = 'Date Opened'

    time_date_submitted.admin_order_field = 'date_submitted'
    time_date_submitted.short_description = 'Date Submitted'
    
    def get_history_view_url(self, obj):
        return reverse('view_history') + f'?uuid={obj.uuid}'
    
    
class CategoryoneAdminForm2(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categoryone2
        fields = ['name', 'task_company','client','date_today','month_submit',  'date_opened', 'date_submitted','is_completed', 'company', 'question_1', 'question_2', 'question_3','question_4', 'question_5', 'question_6', 'question_7', 'question_8']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }


class CategoryoneAdmin2(admin.ModelAdmin):
    form = CategoryoneAdminForm2
    list_display = ('id', 'name', 'elapsed_time', 'time_date_opened', 'time_date_submitted', 'is_completed')
    
    def time_date_opened(self, obj):
        if obj.date_opened is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_opened.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''

    def time_date_submitted(self, obj):
        if obj.date_submitted is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_submitted.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''
    
    time_date_opened.admin_order_field = 'date_opened'
    time_date_opened.short_description = 'Date Opened'

    time_date_submitted.admin_order_field = 'date_submitted'
    time_date_submitted.short_description = 'Date Submitted'
    
class CategoryoneAdminForm3(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categoryone3
        fields = ['name', 'task_company','client','date_today','month_submit',  'date_opened', 'date_submitted', 'is_completed', 'company',
                    'question_1', 'question_2', 'question_3','question_4','question_5',
                    'question_6', 'question_7', 'question_8','question_9', 'question_10',
                    'question_11', 'question_12', 'question_13', 'question_14', 'question_15', 'question_16', 
                    'question_17', 'question_18', 'question_19', 'question_20', 'question_21', 'question_22',
                    'question_23', 'question_24','elapsed_time']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }

class CategoryoneAdmin3(admin.ModelAdmin):
    form = CategoryoneAdminForm3
    list_display = ('id', 'name', 'elapsed_time', 'time_date_opened', 'time_date_submitted', 'is_completed')

    def time_date_opened(self, obj):
        if obj.date_opened is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_opened.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''

    def time_date_submitted(self, obj):
        if obj.date_submitted is not None:
            pst = pytz.timezone('Asia/Manila')
            pst_time = obj.date_submitted.astimezone(pst)
            return pst_time.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''

    time_date_opened.admin_order_field = 'date_opened'
    time_date_opened.short_description = 'Date Opened'

    time_date_submitted.admin_order_field = 'date_submitted'
    time_date_submitted.short_description = 'Date Submitted'
    
    


## Register the models into the admin view site ## 
admin.site.register(User, CustomUserAdmin)
admin.site.register(RequestEdit, RequestEditAdmin)
admin.site.register(Categoryone, CategoryoneAdmin)
admin.site.register(Categoryone2, CategoryoneAdmin2)
admin.site.register(Categoryone3, CategoryoneAdmin3)

##----------------------------------------------##

## END Django Admin View ##

##----------------------------------------------##
