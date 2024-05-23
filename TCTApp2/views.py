from django.contrib.auth.decorators import login_required
from django.apps import apps
from TCTApp.models import *
from TCTApp2.models import *
from django.contrib import messages
from django.shortcuts import render, redirect  
from .forms import * 
from django.core.mail import EmailMessage
import logging
from django.utils import timezone
from datetime import datetime
import pytz
from django.http import JsonResponse


## TASKS ##

manila_tz = pytz.timezone('Asia/Manila')

@login_required
def start_Categorytwo_task(request):
    user = request.user
    view = request.GET.get('view')    
    if request.method == 'POST':
        form = CategorytwoForm(request.POST, elapsed_time=request.POST.get('elapsed_time'))
        if form.is_valid():
            task = form.save(commit=False)
            task.task_company = 'Example Form 1'
            date_submitted = timezone.now().astimezone(manila_tz)
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date
            except ValueError:
                raise ValidationError('Invalid date format')
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.client = 'Form Category 1'
            task.date_today = datetime.now().strftime('%Y%m%d') 
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            
            is_paused = request.POST.get('is_paused')
            if is_paused is None:
                # Check for empty fields if is_paused is None
                for field in form:
                    if not field.value():
                        form.add_error(field.name, f'{field.label} field is required.')

                if form.errors:
                    return JsonResponse({'success': False, 'errors': form.errors})
            
            if is_paused is not None:
                task.is_completed = False
                task.save()
                messages.success(request, 'Task paused successfully!')
                return redirect('index')
            else:
                task.is_completed = True
                task.save()
                messages.success(request, 'Task submitted successfully!')
                return JsonResponse({'success': True, 'redirect_url': '/'})
    else:
        task_seg = request.GET.get('task_segment')
        user = request.user
        view = request.GET.get('view')    
        form = CategorytwoForm(initial={'name':f"{user.first_name} {user.last_name}",'task_segment': task_seg})
        request.session['date_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'form': form,
        'date_opened': request.session.get('date_opened', None),
        'task' : 'Example Form 1',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'view': view,
    }
    return render(request, 'start_task.html', context)

@login_required
def start_Categorytwo_task2(request):
    user = request.user
    view = request.GET.get('view')    
    if request.method == 'POST':
        form = CategorytwoForm2(request.POST, elapsed_time=request.POST.get('elapsed_time'))    
        if form.is_valid():
            task = form.save(commit=False)
            task.task_company = 'Example Form 2'
            date_submitted = timezone.now().astimezone(manila_tz)
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date
            except ValueError:
                raise ValidationError('Invalid date format')
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.client = 'Form Category 1'
            task.date_today = datetime.now().strftime('%Y%m%d') 
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            is_paused = request.POST.get('is_paused')
            if is_paused is None:
                # Check for empty fields if is_paused is None
                for field in form:
                    if not field.value():
                        form.add_error(field.name, f'{field.label} field is required.')

                if form.errors:
                    return JsonResponse({'success': False, 'errors': form.errors})
            
            if is_paused is not None:
                task.is_completed = False
                task.save()
                messages.success(request, 'Task paused successfully!')
                return redirect('index')
            else:
                task.is_completed = True
                task.save()
                messages.success(request, 'Task submitted successfully!')
                return JsonResponse({'success': True, 'redirect_url': '/'})
    else:
        task_seg = request.GET.get('task_segment')
        user = request.user
        view = request.GET.get('view')    
        form = CategorytwoForm2(initial={'name':f"{user.first_name} {user.last_name}",'task_segment': task_seg})
        request.session['date_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'form': form,
        'date_opened': request.session.get('date_opened', None),
        'task' :'Example Form 2',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'view': view,
    }
    return render(request, 'start_task.html', context)

@login_required
def start_Categorytwo_task3(request):
    user = request.user
    view = request.GET.get('view')    
    if request.method == 'POST':
        form = CategorytwoForm3(request.POST, elapsed_time=request.POST.get('elapsed_time'))
        if form.is_valid():
            task = form.save(commit=False)
            task.task_company = 'Example Form 3'
            date_submitted = timezone.now().astimezone(manila_tz)
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date
            except ValueError:
                raise ValidationError('Invalid date format')
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.client = 'Form Category 3'
            task.date_today = datetime.now().strftime('%Y%m%d') 
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            is_paused = request.POST.get('is_paused')
            if is_paused is None:
                # Check for empty fields if is_paused is None
                for field in form:
                    if not field.value():
                        form.add_error(field.name, f'{field.label} field is required.')

                if form.errors:
                    return JsonResponse({'success': False, 'errors': form.errors})
            
            if is_paused is not None:
                task.is_completed = False
                task.save()
                messages.success(request, 'Task paused successfully!')
                return redirect('index')
            else:
                task.is_completed = True
                task.save()
                messages.success(request, 'Task submitted successfully!')
                return JsonResponse({'success': True, 'redirect_url': '/'})
    else:
        task_seg = request.GET.get('task_segment')
        user = request.user
        view = request.GET.get('view')    
        form = CategorytwoForm3(initial={'name':f"{user.first_name} {user.last_name}",'task_segment': task_seg})
        request.session['date_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'form': form,
        'date_opened': request.session.get('date_opened', None),
        'task' : 'Example Form 3',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'view': view,
    }
    return render(request, 'start_task.html', context)

