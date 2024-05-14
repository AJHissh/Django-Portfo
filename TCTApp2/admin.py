from django.contrib import admin
from .forms import *
from .models import *
from django import forms
import pytz
from simple_history.admin import SimpleHistoryAdmin



class CategorytwoAdminForm(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categorytwo
        fields = ['name',  'date_opened', 'date_submitted','is_completed', 'company','date_today', 'month_submit', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'elapsed_time']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }

class CategorytwoAdmin(SimpleHistoryAdmin):
    form = CategorytwoAdminForm
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
    
    
class CategorytwoAdminForm2(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categorytwo2
        fields = ['name',  'date_opened', 'date_submitted', 'is_completed','date_today', 'month_submit', 'question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'elapsed_time']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }

class CategorytwoAdmin2(admin.ModelAdmin):
    form = CategorytwoAdminForm2
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
    
    
class CategorytwoAdminForm3(forms.ModelForm):
    elapsed_time = forms.DurationField()

    class Meta:
        model = Categorytwo3
        fields = ['name',  'date_opened', 'date_submitted', 'is_completed', 
                   'date_today', 'month_submit', 'question_1', 'question_2', 'question_3', 'question_4', 'elapsed_time']
        widgets = {
            'elapsed_time': forms.HiddenInput(),
        }

class CategorytwoAdmin3(admin.ModelAdmin):
    form = CategorytwoAdminForm3
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


admin.site.register(Categorytwo, CategorytwoAdmin)
admin.site.register(Categorytwo2, CategorytwoAdmin2)
admin.site.register(Categorytwo3, CategorytwoAdmin3)

