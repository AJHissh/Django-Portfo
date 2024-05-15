from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from itertools import chain
from TCTApp.models import *
from TCTApp2.models import *
from .forms import * 
from TCTApp2.forms import *
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site  
from .tokens import account_activation_token  
from django.core.mail import EmailMessage
import logging
from django.utils import timezone
from datetime import datetime, timedelta, date
from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.context_processors import csrf
from django.http import Http404
from django.apps import apps
from django.shortcuts import get_object_or_404, render, redirect
from django.forms import modelform_factory
from django.db.models.fields import UUIDField
from uuid import UUID
from simple_history.utils import get_history_manager_for_model
from .decorators import admin_only
import csv
import pytz
from django.core.cache import cache
from django.http import JsonResponse
from pathlib import Path
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
import json
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps
import matplotlib.pyplot as plt
import base64
import io
from collections import defaultdict
from django.conf import settings
from django.templatetags.static import static



class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# creds_path = os.path.join(os.getcwd(), 'secrets', 'green-talent-369202-3636d6d41e91.json')
# creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
# client = gspread.authorize(creds)
init = timezone.now()

##----------------------------------------------##

## DASHBOARD MAIN PAGE ##

##----------------------------------------------##


def index(request):
    user = request.user
    cache_key = None 

    # Get or create a cache key for the user
    if request.user.is_authenticated:
        cache_key = f'index_{str(user.uuid)}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data
    
    # Initialize counts for data needed in dashboard
    today_count = 0
    today_paused_count = 0
    total_paused = 0
    Categorytwo_count = 0
    Categoryone_count = 0
    total_form_completes = 0
    task_dates = defaultdict(list)  # Dictionary to store task counts per date

    # Excluded models from calculations
    excluded_models = ['RequestEdit', 'User', 'HistoricalCategorytwo', 'HistoricalCategorytwo2','HistoricalCategorytwo3','HistoricalCategoryone', 'HistoricalCategoryone2','HistoricalCategoryone3']
    
    # if a user is logged in - go through all apps models except for the ones in the excluded_models list and look for any models with a 'date_opened' and 'date_submitted' field
    if request.user.is_authenticated:
        for model in apps.get_models():
            if (hasattr(model, 'date_opened') and hasattr(model, 'date_submitted')
                and model.__name__ not in excluded_models):

                # Create queries for the data
                query = Q(user=str(user.uuid)) & Q(is_completed=True) 
                
                # Use queries to filter the data and store results
                model_results = model.objects.filter(query)
                
                # Add the count of records found into the count variables above
                if model_results:
                    if hasattr(model, 'date_submitted'):
                        # Count tasks and fetch their submission dates
                        for task in model_results:
                            if task.is_completed:
                                today_count += 1
                            else:
                                today_paused_count += 1
                            if task.date_submitted:
                                task_date = task.date_submitted.date()
                                task_dates[task_date].append(task)
                
    # Prepare data for plotting
    data = {
        'Date Submitted': [],  # Dates submitted
        'Task Count': []  # Count of tasks for each submission date
    }

    # Aggregate task counts per date
    for date_submitted, tasks in task_dates.items():
        data['Date Submitted'].append(date_submitted.strftime('%Y-%m-%d'))
        data['Task Count'].append(len(tasks))

    # Fetch the selected filtering criteria from the request
    selected_day = request.GET.get('selected_day')
    selected_date_range_start = request.GET.get('selected_date_range_start')
    selected_date_range_end = request.GET.get('selected_date_range_end')

    # Filter the data based on the selected criteria
    if selected_day:
        selected_day_tasks = task_dates.get(datetime.strptime(selected_day, '%Y-%m-%d').date(), [])
        data['Date Submitted'] = [selected_day]
        data['Task Count'] = [len(selected_day_tasks)]
    elif selected_date_range_start and selected_date_range_end:
        filtered_dates = []
        filtered_counts = []
        start_date = datetime.strptime(selected_date_range_start, '%Y-%m-%d').date()
        end_date = datetime.strptime(selected_date_range_end, '%Y-%m-%d').date()
        for date_submitted, count in zip(data['Date Submitted'], data['Task Count']):
            date_submitted = datetime.strptime(date_submitted, '%Y-%m-%d').date()
            if start_date <= date_submitted <= end_date:
                filtered_dates.append(date_submitted.strftime('%Y-%m-%d'))
                filtered_counts.append(count)
        data['Date Submitted'] = filtered_dates
        data['Task Count'] = filtered_counts
    
    
    total_form_completes = data['Task Count']
    
    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.bar(data['Date Submitted'], data['Task Count'])
    plt.xlabel('Date Submitted')
    plt.ylabel('Task Count')
    plt.title('Task Count per Day')
    plt.xticks(rotation=45)

    # Saving the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the image as base64
    graph = base64.b64encode(image_png).decode('utf-8')

    # Add the encoded image to the context
    if len(total_form_completes) >= 1:
        context = {
        "user": user,
        'task_count': total_form_completes[0],
        'paused_count': total_paused,
        'submit_today': today_count,
        'paused_today': today_paused_count,
        'Categorytwo_count': Categorytwo_count,
        'Categoryone_count': Categoryone_count,
        'graph': graph  # Add the graph to the context
    }
    else:
        context = {
        "user": user,
        'task_count': 0,
        'paused_count': total_paused,
        'submit_today': today_count,
        'paused_today': today_paused_count,
        'Categorytwo_count': Categorytwo_count,
        'Categoryone_count': Categoryone_count,
        'graph': graph  # Add the graph to the context
    }

    ## Store page render in cache so cache will be rendered instead ##
    rendered_template = render(request, "index.html", context)
    
    ## Returns cache for index view and deletes cache every 5 seconds ##
    if cache_key:
        cache.set(cache_key, rendered_template, 5)  
    return rendered_template


def download_resume(request):
    # Path to your resume file in the static directory
    resume_path = Path(settings.STATIC_ROOT) / 'resume' / 'Andrew_James_Hisshion_Resume_2024_mod.pdf'

    # Open the file in binary mode for reading
    with open(resume_path, 'rb') as resume_file:
        response = HttpResponse(resume_file.read(), content_type='application/pdf')

    # Set the Content-Disposition header to force download
    response['Content-Disposition'] = 'attachment; filename="Andrew_James_Hisshion_Resume_2024_mod.pdf"'
    return response
    


##----------------------------------------------##

## END MAIN DASHBOARD PAGE ##

##----------------------------------------------##

##################################################

##----------------------------------------------##

## ADMIN VIEWS @admin_only decorator ##

##----------------------------------------------##



## ADMIN DATE FILTER VIEW ##


## Retrieves data from data range filter on record tables to query database for data within a 'start' and 'end' date range ##
@admin_only
def admin_date_filter(request):
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')  
    
    ## If 'start' and 'end' exists -  convert 'start' and 'end' time from requests to proper time format for database query ##
    if start and end:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        logging.debug(start_date)
        
        ## Excluded models with data not required for these calculations ##
        excluded_models = ['RequestEdit', 'User', 'HistoricalCategorytwo', 'HistoricalCategorytwo2','HistoricalCategorytwo3','HistoricalCategorytwo4','HistoricalCategorytwo5','HistoricalCategorytwo6','HistoricalCategorytwo7','HistoricalCategorytwo8','HistoricalCategorytwo9','HistoricalCategorytwo10','HistoricalCategorytwo11','HistoricalCategorytwo12','HistoricalCategorytwo13',
                           'HistoricalCategoryone', 'HistoricalCategoryone2','HistoricalCategoryone3','HistoricalCategoryone4','HistoricalCategoryone5','HistoricalCategoryone6','HistoricalCategoryone7','HistoricalCategoryone8','HistoricalCategoryone9','HistoricalCategoryone10','HistoricalCategoryone11','HistoricalCategoryone12','HistoricalCategoryone13','HistoricalCategoryone14','HistoricalCategoryone15','HistoricalCategoryone16','HistoricalCategoryone17','HistoricalCategoryone18','HistoricalCategoryone19','HistoricalCategoryone20']

        ## Creates list to store list of data retrieved from database query ##
        table_rows = []
        
        ## Set variable to store timezone that is going to be used to retrieve the correct time ##
        local_tz = pytz.timezone('Asia/Manila')

        ## if a user is logged in - go through all apps models except for the ones in the excluded_models list and look for any models with a 'date_opened' and 'date_submitted' field ##
        for model in apps.get_models(): 
            if (hasattr(model, 'date_opened') and hasattr(model, 'date_submitted')
                and model.__name__ not in excluded_models):

                ## Creates a query for the database using __range method with 'start_date' and 'end_date' ## 
                query = Q(date_opened__date__range=(start_date, end_date)) | Q(date_submitted__date__range=(start_date, end_date))
                
                ## Uses query to filter objects with the models and retrieve that data ##
                model_results = model.objects.filter(query)
                if model_results:
                    for record in model_results:
                        row = []
                        for field in model._meta.fields:
                            ## If a field in my models is a datetime field - get that record and convert the datetime field to proper formats ex. 'Asia/Manila' timezone, Hour:Minutes:Seconds. etc ## 
                            if isinstance(field, models.DateTimeField):
                                dt = getattr(record, field.name)
                                dt_local = dt.astimezone(local_tz)
                                date_str = dt_local.strftime('%B %d, %Y')
                                time_str = dt_local.strftime('%#I:%M:%S %p').lower().replace('am', 'a.m.').replace('pm', 'p.m.')
                                # Stores the new formatted data strings into the value variable ##
                                value = f"{date_str} {time_str}"
                            else:
                                value = getattr(record, field.name)
                            ## Stores the value variable inside the row list ##   
                            row.append(value)
                        ## Stores the row list within the tables_rows list ##
                        table_rows.append(row)
        
        ## Sorts table rows list by the column at index[1] which is date_opened and then stores newly sorted data within 'date_data' - which should be data within a specific date range ##                 
        date_data = sorted(table_rows, key=lambda x: x[0], reverse=True)
        
        ## If there is data within the 'start' and 'end' variables - get the length max length of an objects data and set that as max_columns ## 
        ## This is so all records in the table will have an equal amount of cells in the table ##
        if start and end:
            try:
                max_columns = max(len(row) for row in date_data if any(row))
            except:
                max_columns = len(date_data)

            ## Converts each record in date_data into a list ##
            date_data = [list(row) for row in date_data]

            ## Go each record in data_data - go to the column at index[3] which is the elapsed_time column and convert the format of elapsed_time into time in minutes[] and store in back within the elapsed_time column ##
            for i in range(len(date_data)):
                time_str = str(date_data[i][3])
                time_obj = datetime.strptime(time_str, '%H:%M:%S')
                time_in_minutes = round((time_obj.hour * 60) + time_obj.minute + (time_obj.second / 60), 2)
                date_data[i][3] = time_in_minutes

            ## Converts records into tuples ##
            date_data = [tuple(row) for row in date_data]
            
            ## Adds blank values to records without less data than the record with the max/most columns and converts the record back into a list ##
            date_data = [list(row) + [''] * (max_columns - len(row)) for row in date_data]
            
            ## Stores date_data in paginator class object with 50 records per page ## 
            paginator = Paginator(date_data, 50) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            data_filter = page_obj

            ## If there are any errors in storing the queried data it most likely is a data out of range issue and if there are none, render the data within the date range ##
            try:
                    context = {
                'data_filter': data_filter,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'start': start,
                'end': end,
                }

            except:
                    context = {
            'error_message':'Data is out of range',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            return render(request, 'admin_date_filter.html', context)
    return HttpResponseRedirect('/admin_view_records') 
        
      


## ADMIN VIEW ALL RECORDS VIEW ##

@admin_only
def admin_view_records(request):
    
    ## Retrieves search_query string from request if present and stores in within the search query variable ##
    search_query = request.GET.get('search_query') 
    
    ## If there data within search_query store the following queries into query variables ex. Categorytwo_query, Categoryone_query etc. ## 
    if search_query is not None:
        Categorytwo_query =  Q(client__icontains=search_query) | Q(id__icontains=search_query)  | Q(task_company__icontains=search_query) | Q(task_segment__icontains=search_query) | Q(date_today__icontains=search_query) | Q(month_submit__icontains=search_query)  
        Categoryone_query = Q(client__icontains=search_query) | Q(id__icontains=search_query)  | Q(task_company__icontains=search_query) | Q(task_segment__icontains=search_query) | Q(date_today__icontains=search_query) | Q(month_submit__icontains=search_query) 
    else:
    ## If there is no data within search_query,store the query variables without query parameters ## 
        Categorytwo_query = Q()
        Categoryone_query = Q()

    ## Use the query variable to filter through each object within each model in the chain and store data that meets the queries paramters within the data variable ex. Categorytwo_data, Categoryone_data etc. ## 
    Categorytwo_data = list(chain(Categorytwo.objects.filter(Categorytwo_query).values_list(), Categorytwo2.objects.filter(Categorytwo_query).values_list(), Categorytwo3.objects.filter(Categorytwo_query).values_list()))

    Categoryone_data = list(chain(Categoryone.objects.filter(Categoryone_query).values_list(), Categoryone2.objects.filter(Categoryone_query).values_list(),
                          Categoryone3.objects.filter(Categoryone_query).values_list()))
    
    
    ## Combines all data from queried data and sorts the data by the column at index[1] which is the 'date_opened' field and then stores the sorted data into the 'data' variable ##
    data = sorted(chain(Categorytwo_data , Categoryone_data), key=lambda x: x[3], reverse=True)
    
    try:
        max_columns = max(len(row) for row in data if any(row))
    except:
        max_columns = len(data)
        
    data = [list(row) for row in data]
    
    for i in range(len(data)):
        time_str = str(data[i][4])
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        time_in_minutes = round((time_obj.hour * 60) + time_obj.minute + (time_obj.second / 60), 2)
        data[i][4] = time_in_minutes
        
    data = [tuple(row) for row in data]

    data = [list(row) + [''] * (max_columns - len(row)) for row in data]
    empty_columns = [i for i in range(max_columns) if all(not row[i] for row in data)]
 
    paginator = Paginator(data, 50) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    try:
        context = {
        'data': page_obj,
        'max_columns': max_columns,
        'empty_columns': empty_columns,
        'num_missing_columns': max(0, max_columns - len(data[0])) if data else 0,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    except:
        context = {
        'error_message':'Data is out of range',
        'max_columns': max_columns,
        'empty_columns': empty_columns,
        'num_missing_columns': max(0, max_columns - len(data[0])) if data else 0,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    logging.debug(data)
    return render(request, 'admin_view_records.html', context)

@admin_only
def admin_edit_records(request):
    ## Gets string sent as 'record_id' from request and stores in within the record_id variable ##
    record_id = request.GET.get('record_id')
    
    ## Iterates through all apps models if there is a UUID present and stores those models into 'uuid_models' ##
    uuid_models = [model for model in apps.get_models() if model._meta.pk.primary_key and isinstance(model._meta.pk, UUIDField)]
    
    ## Iterates through 'uuid_models' and searches for objects within the models with a record id which matches the UUID stored in the 'record_id' variable - If there is no matching record return 'Invalid Record ID!'##
    for model in uuid_models:
        try:
            task = model.objects.filter(id=record_id).get()
            TaskForm = modelform_factory(model, exclude=[''])
            form = TaskForm(request.POST or None, instance=task)
            break
        except model.DoesNotExist:
            continue
    else:
        messages.success(request, 'Invalid Record ID!')
        return redirect('index')
    
    if request.method == 'POST':
        ## if there is a POST request and the 'delete_record' string is within that request - get the model with the matching UUID and delete it ##
        if 'delete_record' in request.POST:
            task = model.objects.get(id=record_id)
            task.delete()
            messages.success(request, 'Task Deleted Successfully!')
            return redirect('index')
        ## if there is a POST request and the 'delete_record' string is not within that request - check if the form is valid and then submit the form data ##
        elif form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, 'Task Edited Successfully!')
            return redirect('index')
    
    ## Stores form data retrieved from uuid_models loop into 'form' variable for rendering in admin_edit_records.html if record id is valid ## 
    context = {
        'form': form,
        'date_opened': request.session.get('date_opened', None),
        'company': task.task_company,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'id':record_id,
    }    
    return render(request, 'admin_edit_records.html', context)

    
@admin_only
def admin_view_history(request):
    ## Stores the value from 'record_id' in the request for use in the query ## 
    record_id = request.GET.get('record_id')

    ## Iterate through all the models in all apps ## 
    for model in apps.get_models():
        # Check if the model's primary key is a UUIDField
        if not model._meta.pk.is_relation and model._meta.pk.__class__.__name__ == 'UUIDField':
            try:
                ## Stores records from models where its UUID matches the 'record_id' sent in the request ##
                obj = model.objects.get(id=UUID(record_id))
                ## Gets Historical data for each model then filters it using the UUID of the record from the obj data stored above and stores the historical data for the record in the 'history_list' variable ## 
                history_manager = get_history_manager_for_model(model)
                history_list = history_manager.filter(id=obj.id)
                
                ## Create changes list for storing record history data ##
                changes = []
                
                # Iterate through the historical records
                for h in history_list:
                    # Create dictionary to store version data 
                    version = {}
                    # Iterate through the fields of the record
                    for field in obj._meta.fields:
                        # Get value of field and store in the version dictionary ## 
                        version[field.name] = getattr(h.instance, field.name)
                    changes.append(version)
                    
                # Remove duplicates from the changes list    
                changes = [tuple(d.items()) for d in changes] 
                changes = list(set(changes))  
                changes = [dict(t) for t in changes]
                # Sort changes based on 'elapsed_time' field
                changes = sorted(changes, key=lambda x: x['elapsed_time'], reverse=True)
                
                # Create a paginator for changes with 50 records per page
                paginator = Paginator(changes, 50) 
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)  
                context = {
                    'obj': obj,
                    'changes': page_obj,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }  
                return render(request, 'admin_view_history.html', context)
            except model.DoesNotExist:
                pass
    # If no history found for the record id, display a message and redirect to the index page
    messages.success(request, f'No history found for record id {record_id}')
    return redirect('index')

@admin_only
def download_records(request):
    manila_timezone = pytz.timezone('Asia/Manila')
    date = datetime.now().astimezone(manila_timezone).strftime('%Y-%m-%d')
    # Get the current date
    date_now = datetime.now().strftime('%Y-%m-%d')
    # Create an HTTP response object with CSV content type
    response = HttpResponse(content_type='text/csv')
    # Set the content disposition to be an attachment and set the filename for the response
    response['Content-Disposition'] = f'attachment; filename="all-records-{date_now}_no_version_history.csv"'
    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Query and retrieve data from Categorytwo models, Categoryone models##
    Categorytwo_query = Q()
    Categorytwo_data = list(chain(Categorytwo.objects.filter(Categorytwo_query).values_list(), Categorytwo2.objects.filter(Categorytwo_query).values_list(), Categorytwo3.objects.filter(Categorytwo_query).values_list()))

    Categoryone_query = Q()
    Categoryone_data = list(chain(Categoryone.objects.filter(Categoryone_query).values_list(), Categoryone2.objects.filter(Categoryone_query).values_list(),
                          Categoryone3.objects.filter(Categoryone_query).values_list()))

    # Combine all the data into one list
    data = sorted(chain(Categorytwo_data , Categoryone_data), key=lambda x: x[3])
    
    # Convert each row of data into a list
    data = [list(row) for row in data] 
    
    # Convert time field to minutes
    for i in range(len(data)):
        time_str = str(data[i][4])
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        time_in_minutes = round((time_obj.hour * 60) + time_obj.minute + (time_obj.second / 60), 2)
        data[i][4] = time_in_minutes
        
        # Convert data[i][2] (column 2) to Manila time zone
        datetime_obj2 = data[i][2].astimezone(manila_timezone)
        data[i][2] = datetime_obj2
        
        # Convert data[i][3] (column 3) to Manila time zone
        datetime_obj3 = data[i][3].astimezone(manila_timezone)
        data[i][3] = datetime_obj3
        
        
    
    data = [tuple(row) for row in data]

    # Write the data to the CSV file
    for dat in data:
        writer.writerow([str(field_value) for field_value in dat])
        
    # Clear the existing_rows list
    existing_rows = []
    
    # Get the existing rows from the spreadsheet
    existing_rows = sheet1.get_all_values()

    unique_col_index = 7

    # Create a set to store the unique identifiers of existing rows
    existing_identifiers = set(row[unique_col_index] for row in existing_rows)
    
    logging.debug(existing_identifiers)

    # Convert data_list unique identifiers to strings
    data_list = [list(row) for row in data]
    data_list = [[str(value) for value in row] for row in data_list]

    # Filter the data to include only rows not in the existing spreadsheet
    new_data = [row for row in data_list if str(row[unique_col_index]) not in existing_identifiers]

    # Append the new_data to the existing rows
    existing_rows += new_data

    # Serialize the updated rows to JSON
    json_data = json.dumps(existing_rows, cls=CustomJSONEncoder)

    # Clear the existing rows in the spreadsheet
    sheet1.clear()

    # Deserialize the JSON data
    deserialized_data = json.loads(json_data)

    # Append the updated rows to the spreadsheet
    sheet1.append_rows(deserialized_data)

    # Update the existing_identifiers with the unique identifiers from the newly appended rows
    existing_identifiers.update(row[unique_col_index] for row in deserialized_data)

    # Return the HTTP response containing the CSV file
    return response










### CLIENT DOWNLOAD RECORDS VIEWS### 
@admin_only 
def Categoryone_download_records(request):
    manila_timezone = pytz.timezone('Asia/Manila')
    date = datetime.now().astimezone(manila_timezone).strftime('%Y-%m-%d')
    # Get the current date in the format 'YYYY-MM-DD'
    date_now = datetime.now().strftime('%Y-%m-%d')
    # Create an HTTP response object with content type 'text/csv'
    response = HttpResponse(content_type='text/csv')
    # Set the content disposition to be an attachment and set the filename for the response
    response['Content-Disposition'] = f'attachment; filename="Categoryone-records-{date_now}_no_version_history.csv"'
    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Fetch data from multiple Categoryone models and concatenate them into a single list
    Categoryone_query = Q()
    Categoryone_data = list(chain(Categoryone.objects.filter(Categoryone_query).values_list(), Categoryone2.objects.filter(Categoryone_query).values_list(),
                          Categoryone3.objects.filter(Categoryone_query).values_list()))
    
    # Sort the data based on the second element of each tuple
    data = sorted(chain(Categoryone_data), key=lambda x: x[3])
    
    # Convert the data to a list of lists
    data = [list(row) for row in data] 
    
    # Convert the time in the fourth or index[3] column to minutes
    for i in range(len(data)):
        time_str = str(data[i][4])
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        time_in_minutes = round((time_obj.hour * 60) + time_obj.minute + (time_obj.second / 60), 2)
        data[i][4] = time_in_minutes
        
        # Convert data[i][2] (column 2) to Manila time zone
        datetime_obj2 = data[i][2].astimezone(manila_timezone)
        data[i][2] = datetime_obj2
        
        # Convert data[i][3] (column 3) to Manila time zone
        datetime_obj3 = data[i][3].astimezone(manila_timezone)
        data[i][3] = datetime_obj3
    
    # Convert the data back to a list of tuples
    data = [tuple(row) for row in data]
    
    # Write each row of data to the CSV file
    for dat in data:
        writer.writerow([str(field_value) for field_value in dat])
        
    # Clear the existing_rows list
    existing_rows = []
    
    # Get the existing rows from the spreadsheet
    existing_rows = sheet3.get_all_values()

    unique_col_index = 7

    # Create a set to store the unique identifiers of existing rows
    existing_identifiers = set(row[unique_col_index] for row in existing_rows)
    
    logging.debug(existing_identifiers)

    # Convert data_list unique identifiers to strings
    data_list = [list(row) for row in data]
    data_list = [[str(value) for value in row] for row in data_list]

    # Filter the data to include only rows not in the existing spreadsheet
    new_data = [row for row in data_list if str(row[unique_col_index]) not in existing_identifiers]

    # Append the new_data to the existing rows
    existing_rows += new_data

    # Serialize the updated rows to JSON
    json_data = json.dumps(existing_rows, cls=CustomJSONEncoder)

    # Clear the existing rows in the spreadsheet
    sheet3.clear()

    # Deserialize the JSON data
    deserialized_data = json.loads(json_data)

    # Append the updated rows to the spreadsheet
    sheet3.append_rows(deserialized_data)

    # Update the existing_identifiers with the unique identifiers from the newly appended rows
    existing_identifiers.update(row[unique_col_index] for row in deserialized_data)

    # Return the HTTP response containing the CSV file
    return response
    

       
    
@admin_only 
def Categorytwo_download_records(request):
    manila_timezone = pytz.timezone('Asia/Manila')
    date = datetime.now().astimezone(manila_timezone).strftime('%Y-%m-%d')
    date_now = datetime.now().strftime('%Y-%m-%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Categorytwo-records-{date_now}_no_version_history.csv"'
    writer = csv.writer(response)
    
    Categorytwo_query = Q()
    Categorytwo_data = list(chain(Categorytwo.objects.filter(Categorytwo_query).values_list(), Categorytwo2.objects.filter(Categorytwo_query).values_list(), Categorytwo3.objects.filter(Categorytwo_query).values_list()))
    
    data = sorted(chain(Categorytwo_data), key=lambda x: x[3])
    
    data = [list(row) for row in data] 
    
    for i in range(len(data)):
        time_str = str(data[i][4])
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        time_in_minutes = round((time_obj.hour * 60) + time_obj.minute + (time_obj.second / 60), 2)
        data[i][4] = time_in_minutes
        
        # Convert data[i][2] (column 2) to Manila time zone
        datetime_obj2 = data[i][2].astimezone(manila_timezone)
        data[i][2] = datetime_obj2
        
        # Convert data[i][3] (column 3) to Manila time zone
        datetime_obj3 = data[i][3].astimezone(manila_timezone)
        data[i][3] = datetime_obj3
    
    data = [tuple(row) for row in data]
        
    for dat in data:
        writer.writerow([str(field_value) for field_value in dat])
        
    # Clear the existing_rows list
    existing_rows = []
    
    # Get the existing rows from the spreadsheet
    existing_rows = sheet4.get_all_values()

    unique_col_index = 7

    # Create a set to store the unique identifiers of existing rows
    existing_identifiers = set(row[unique_col_index] for row in existing_rows)
    
    logging.debug(existing_identifiers)

    # Convert data_list unique identifiers to strings
    data_list = [list(row) for row in data]
    data_list = [[str(value) for value in row] for row in data_list]

    # Filter the data to include only rows not in the existing spreadsheet
    new_data = [row for row in data_list if str(row[unique_col_index]) not in existing_identifiers]

    # Append the new_data to the existing rows
    existing_rows += new_data

    # Serialize the updated rows to JSON
    json_data = json.dumps(existing_rows, cls=CustomJSONEncoder)

    # Clear the existing rows in the spreadsheet
    sheet4.clear()

    # Deserialize the JSON data
    deserialized_data = json.loads(json_data)

    # Append the updated rows to the spreadsheet
    sheet4.append_rows(deserialized_data)

    # Update the existing_identifiers with the unique identifiers from the newly appended rows
    existing_identifiers.update(row[unique_col_index] for row in deserialized_data)

    # Return the HTTP response containing the CSV file
    return response

    
### END CLIENT DOWNLOAD RECORDS ### 
    
@admin_only
def download_records_all_version(request):
    date = datetime.now().strftime('%Y-%m-%d')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename= "all-records-{date}_version_history.csv"'
    writer = csv.writer(response)

    # Iterate over all models in all apps
    for model in apps.get_models():
        # Skip models from the 'admin' app and the 'RequestEdit' model
        if model._meta.app_label != 'admin' and model.__name__ != 'RequestEdit':
            # Check if the model has a history manager
            history_manager = getattr(model, 'history', None)
            if history_manager:
                # Get the field names of the model
                field_names = [field.name for field in model._meta.fields]
                # Iterate over all objects of the model
                for obj in model.objects.all():
                    # Get the history for the current object
                    history = history_manager.filter(id=obj.id)
                    # Iterate over each version in the history
                    for i, version in enumerate(history):
                        if version.prev_record:
                            # If there is a previous record, compare the values with the current record
                            current_values = [getattr(version.instance, field_name) for field_name in field_names]
                            prev_values = [getattr(version.prev_record, field_name) for field_name in field_names]
                            # Create a list of with the differences between the previous and current values
                            diff = [(field_names[j], prev_values[j], current_values[j]) for j in range(len(field_names)) if prev_values[j] != current_values[j]]
                            # Write the version information, current values, and differences to the CSV file
                            writer.writerow([i+1, version.history_date, version.history_user, version.get_history_type_display()] + current_values + [diff])
                        else:
                            # If there is no previous record, write the version information and current values to the CSV file
                            current_values = [getattr(version.instance, field_name) for field_name in field_names]
                            writer.writerow([i+1, version.history_date, version.history_user, version.get_history_type_display()] + current_values + [None])
    # Return the HTTP response containing the CSV file
    return response

@admin_only
def admin_view_change_requests(request):
    # Gets all records for the RequestEdit model then stores it in the 'edit_reqs' variable for use in context 
    edit_reqs = RequestEdit.objects.all()
    context = {
            'edit_reqs': edit_reqs,
    }
    return render(request, 'admin_view_change_requests.html', context)

@admin_only
def admin_view_change_requests_completion(request):
    # Get the 'record_id' from the request which is the record ID of the RequestEdit record and not the record in which the user wants edited 
    record_id = request.GET.get('record_id')
    
    # Find all models in all apps that have a UUID primary key
    uuid_models = [model for model in apps.get_models() if model._meta.pk.primary_key and isinstance(model._meta.pk, UUIDField)]
    # Iterate over the UUID models
    for model in uuid_models:
        try:
            # Try to fetch the RequestEdit form with the given record_id
            task = model.objects.filter(id=record_id).get()
            # Create a dynamic form for the model, excluding the 'id' field since ID field is only related to the UUID of the RequestEdit form object that is saved when making a edit request
            TaskForm = modelform_factory(model, exclude=['id'])
            # Instantiate the form with the request data and the retrieved form instance
            form = TaskForm(request.POST or None, instance=task)
            break
        except model.DoesNotExist:
            continue
    else:
        # If the task is not found in any model, display an error message and redirect to 'index'
        messages.success(request, 'Invalid Record ID!')
        return redirect('index')
    
    if request.method == 'POST':
        logging.debug(form)
        logging.debug(print(form.errors))
        if form.is_valid():
            logging.debug(form)
            # If the form is valid, save the changes to the task
            task = form.save(commit=False)
            task.save()
            messages.success(request, 'Record Update Request Submitted!')
            return redirect('index')
        else:
            # If the form is not valid, display an error message and redirect to 'index'
            messages.success(request, 'Error Submitting Record Update Request!')
            return redirect('index')
    # Prepare the context with the request_edit and form objects for rendering the template
    context = {'request_edit': request_edit, 'form': form}
    return render(request, 'admin_view_change_requests_completion.html', context)



##----------------------------------------------##

##  END ADMIN VIEWS @admin_only decorator ##

##----------------------------------------------##

    
##################################################


##----------------------------------------------##

## USER VIEWS @login_required decorator ##

##----------------------------------------------##



## VIEW HISTORY VIEW ##

@login_required
def view_history(request):
    # Get the record ID from the request's GET parameters
    record_id = request.GET.get('record_id')
    
    # Iterate through all registered models in the application
    for model in apps.get_models():
        # Check if the model's primary key is a UUIDField
        if not model._meta.pk.is_relation and model._meta.pk.__class__.__name__ == 'UUIDField':
            try:
                # Retrieve the object with the specified record ID
                obj = model.objects.get(id=UUID(record_id))
                
                # Get the history manager for the model
                history_manager = get_history_manager_for_model(model)
                
                # Retrieve the history for the object
                history_list = history_manager.filter(id=obj.id)
                
                # Retrieve the complete history for the object
                history = history_manager.filter(id=obj.id)
                
                changes = []
                
                # Iterate through each historical version in the history list
                for h in history_list:
                    version = {}
                    # Iterate through each field in the object's meta fields
                    for field in obj._meta.fields:
                        # Exclude specific fields from the version (elapsed_time, user)
                        if field.name not in ['elapsed_time', 'user']:
                            # Get the value of the field from the historical instance
                            version[field.name] = getattr(h.instance, field.name)
                    # Add the version to the changes list
                    changes.append(version)
                
                # Convert the changes list to a set of tuples, removing duplicates
                changes = [tuple(d.items()) for d in changes]
                changes = list(set(changes))
                
                # Convert the changes back to a list of dictionaries
                changes = [dict(t) for t in changes]
                
                # Sort the changes based on the 'date_submitted' key in descending order
                changes = sorted(changes, key=lambda x: x['date_submitted'], reverse=True)
                
                # Create a paginator with 50 changes per page
                paginator = Paginator(changes, 50)
                
                # Get the page number from the request's GET parameters
                page_number = request.GET.get('page')
                
                # Get the page object for the specified page number
                page_obj = paginator.get_page(page_number)
                
                # Create a context dictionary with relevant data
                context = {
                    'history': history,
                    'obj': obj,
                    'changes': page_obj,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                
                # Render the 'view_history.html' template with the context
                return render(request, 'view_history.html', context)
            
            except model.DoesNotExist:
                # If the object with the specified record ID does not exist, continue to the next model
                pass
    
    # If no history is found for the record ID, display a success message and redirect to 'index'
    messages.success(request, f'No history found for record id {record_id}')
    return redirect('index')





## END VIEW HISTORY TESTS ##

## LOGIN, REGISTER, ACTIVATION ##

def login_view(request):
    # Check if the request method is POST (i.e., form submission)
    if request.method == "POST":
        # Get the email and password from the POST parameters
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Authenticate the user with the provided email and password
        user = authenticate(request, username=email, password=password)
        
        # Check if the user is authenticated
        if user is not None:
            # Log in the user and redirect to the "index" view
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If authentication fails, render the "login.html" template with an error message
            return render(request, "login.html", {
                "error_message": "Invalid username and/or password."
            })
    else:
        # If the request method is not POST, render the "login.html" template
        return render(request, "login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # Check if the request method is POST (i.e., form submission)
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = SignupForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Create a user object from the form data, but do not save it yet
            user = form.save(commit=False)
            
            # Set the user's active status to False
            user.is_active = True
            
            # Save the user object
            user.save()
            
            # Get the current site for generating the activation link
            current_site = get_current_site(request)
            
            # # Create the subject and message for the activation email
            # mail_subject = 'Activation link has been sent to your email id'
            # message = render_to_string('acc_active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            
            # # Get the email address from the form's cleaned data
            # to_email = form.cleaned_data.get('email')
            
            # # Create an EmailMessage instance with the activation email details
            # email = EmailMessage(
            #     mail_subject, message, to=[to_email],
            #     from_email='andrewjameshisshion@hotmail.com'
            # )
            
            # # Send the activation email
            # email.send()
            messages.success(request,'You have successfully registered. You may now log in')
            
            # Redirect to the "index" view
            return redirect('index')
            
        
             # Display a success message to the user
    else:
        # If the request method is not POST, create an empty form instance
        form = SignupForm()
    
    # Render the "register.html" template with the form instance
    return render(request, 'register.html', {'form': form})


# def activate(request, uidb64, token):
#     # Get the user model
#     User = get_user_model()
    
#     try:
#         # Decode the UID from base64 and get the user with the corresponding UID
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         # If an error occurs during decoding or retrieving the user, set user to None
#         user = None
    
#     # Check if the user is not None and the activation token is valid
#     if user is not None and account_activation_token.check_token(user, token):
#         # Set the user's active status to True
#         user.is_active = True
#         user.save()
        
#         # Display a success message to the user
#         messages.success(request, 'You may now login to your account. Thank you!')
        
#         # Redirect to the "index" view
#         return redirect('index')
#     else:
#         # Display a message indicating that the activation link is invalid
#         messages.success(request, 'Activation Link is Invalid. Please Try Again')
        
#         # Redirect to the "index" view
#         return redirect('index')
 
    
## END LOGIN, REGISTER, ACTIVATION ##

## PROFILE PAGE ##

@login_required
def profile_view(request):
    return render(request, "profile.html")

## REQUEST EDIT ##
@login_required
def request_edit(request):
    # Get the record ID from the request's GET parameters
    record_id = request.GET.get('record_id')
    
    # Get the current user
    user = request.user
    
    # Create a form instance with initial data
    form = RequestEditForm(initial={'record_ID': record_id, 'name': f"{user.first_name} {user.last_name}", 'user_id': user.id})
    
    # Check if the request method is POST 
    if request.method == 'POST':
        # Create a form instance with the POST data
        form = RequestEditForm(request.POST)
        
        # Check if the form is valid
        if form.is_valid():
            # Create a task object from the form data, but do not save it yet
            task = form.save(commit=False)
            
            # Set the record_ID field of the task to the record ID
            task.record_ID = record_id
            
            # Save the task object
            task.save()
            
            # Display a success message to the user
            messages.success(request, 'Record Update Request Submitted!')
            
            # Redirect to the "index" view
            return redirect('index')
    
    # Create a context dictionary with the form instance
    context = {'form': form}
    
    # Render the "request_edit.html" template with the context
    return render(request, "request_edit.html", context)


## END REQUEST EDIT ##     
    
## VIEW ALL RECORDS ##
    
@csrf_protect
@login_required
def view_records(request):
    user = request.user
    user_id = user.uuid
    search_query = request.GET.get('search_query', '').strip()
    company_filter = request.GET.get('company_filter', '').strip()
    start = request.GET.get('start_date', '').strip()
    end = request.GET.get('end_date', '').strip()

    query = Q(user=user_id)
    
    if search_query is not None:
        query &= (Q(client__icontains=search_query) | Q(id__icontains=search_query) | Q(task_company__icontains=search_query) | Q(task_segment__icontains=search_query) | Q(date_today__icontains=search_query) | Q(month_submit__icontains=search_query))

    if company_filter:
        query &= Q(client__icontains=company_filter)

    Categorytwo_data = list(chain(
        Categorytwo.objects.filter(query).values_list(),
        Categorytwo2.objects.filter(query).values_list(),
        Categorytwo3.objects.filter(query).values_list(),
    ))

    Categoryone_data = list(chain(
        Categoryone.objects.filter(query).values_list(),
        Categoryone2.objects.filter(query).values_list(),
        Categoryone3.objects.filter(query).values_list(),
    ))
  
    
    data = sorted(chain(Categorytwo_data, Categoryone_data), key=lambda x: x[3], reverse=True)
         
    if start and end:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
        logging.debug(start_date)
        
        excluded_models = ['RequestEdit', 'User', 'HistoricalCategorytwo', 'HistoricalCategorytwo2','HistoricalCategorytwo3','HistoricalCategorytwo4','HistoricalCategorytwo5','HistoricalCategorytwo6','HistoricalCategorytwo7','HistoricalCategorytwo8','HistoricalCategorytwo9','HistoricalCategorytwo10','HistoricalCategorytwo11','HistoricalCategorytwo12','HistoricalCategorytwo13',
                           'HistoricalCategoryone', 'HistoricalCategoryone2','HistoricalCategoryone3','HistoricalCategoryone4','HistoricalCategoryone5','HistoricalCategoryone6','HistoricalCategoryone7','HistoricalCategoryone8','HistoricalCategoryone9','HistoricalCategoryone10','HistoricalCategoryone11','HistoricalCategoryone12','HistoricalCategoryone13','HistoricalCategoryone14','HistoricalCategoryone15','HistoricalCategoryone16','HistoricalCategoryone17','HistoricalCategoryone18','HistoricalCategoryone19','HistoricalCategoryone20']
        table_rows = []
        local_tz = pytz.timezone('Asia/Manila')

        for model in apps.get_models(): 
            if (hasattr(model, 'date_opened') and hasattr(model, 'date_submitted')
                and model.__name__ not in excluded_models):
                if company_filter:
                    query = Q(date_opened__date__range=(start_date, end_date)) & Q(date_submitted__date__range=(start_date, end_date)) & Q(user=user_id) & Q(client=company_filter)
                if search_query:
                    query = Q(date_opened__date__range=(start_date, end_date)) & Q(date_submitted__date__range=(start_date, end_date)) & Q(user=user_id) & (Q(client=search_query) | Q(task_company=search_query) | Q(task_segment=search_query) | Q(date_today=search_query) | Q(month_submit=search_query))
                else:
                    query = Q(date_opened__date__range=(start_date, end_date)) & Q(date_submitted__date__range=(start_date, end_date)) & Q(user=user_id)
                model_results = model.objects.filter(query)
                if model_results:
                    for record in model_results:
                        row = []
                        for field in model._meta.fields:
                            if isinstance(field, models.DateTimeField):
                                dt = getattr(record, field.name)
                                dt_local = dt.astimezone(local_tz)
                                date_str = dt_local.strftime('%B %d, %Y')
                                time_str = dt_local.strftime('%#I:%M:%S %p').lower().replace('am', 'a.m.').replace('pm', 'p.m.')
                                value = f"{date_str} {time_str}"
                            else:
                                value = getattr(record, field.name)
                            row.append(value)
                        table_rows.append(row)
                        
        data = sorted(table_rows, key=lambda x: x[2], reverse=True)


    data = [list(row) for row in data]

    for row in data:
        del row[4]
        del row[1]

    try:
        max_columns = max(len(row) for row in data if any(row))
    except:
        max_columns = len(data)

    data = [tuple(row) for row in data]

    data = [list(row) + [''] * (max_columns - len(row)) for row in data]
    empty_columns = [i for i in range(max_columns) if all(not row[i] for row in data)]

    column_index = request.GET.get('sort_column')
    reverse_sort = request.GET.get('reverse_sort') == 'true' if request.GET.get('reverse_sort') is not None else False

    if column_index is not None and column_index.isdigit() and int(column_index) < max_columns:
        column_index = int(column_index)
        data = sorted(data, key=lambda x: x[column_index], reverse=reverse_sort)

    paginator = Paginator(data, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Update the pagination links to include the sort parameters
    page_obj.previous_page_link = reverse('view_records') + f'?page={page_obj.previous_page_number}&sort_column={column_index}&reverse_sort={reverse_sort}'
    page_obj.next_page_link = reverse('view_records') + f'?page={page_obj.next_page_number}&sort_column={column_index}&reverse_sort={reverse_sort}'
    
    try:
        context = {
            'data': page_obj,
            'max_columns': max_columns,
            'empty_columns': empty_columns,
            'num_missing_columns': max(0, max_columns - len(data[0])) if data else 0,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reverse_sort': reverse_sort,
            'sort_column': column_index,
            'company_filter': company_filter,
            'search_query': search_query,
            'start': start,
            'end': end,
        }
    except:
        context = {
            'error_message': 'Data is out of range',
            'max_columns': max_columns,
            'empty_columns': empty_columns,
            'num_missing_columns': max(0, max_columns - len(data[0])) if data else 0,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    
    return render(request, 'records.html', context)

## END VIEW ALL RECORDS ##


@login_required
def test(request):   
    return render(request, "test.html")


## RESUME TASKS ##

def get_form_for_model(model_class, data=None, instance=None):
    # Generate a form class dynamically for the given model class
    form_class = forms.modelform_factory(model_class, exclude=[])
    
    # Create an instance of the form class with the provided data and instance
    return form_class(data=data, instance=instance)

@login_required
def resume_tasks(request):
    # Get the current user
    user = request.user
    
    # Get the record ID from the request's GET parameters
    record_id = request.GET.get('record_id', '').strip()
    
    # Initialize task_company to None
    task_company = None
    
    # Find UUID models
    uuid_models = [model for model in apps.get_models() if model._meta.pk.primary_key and isinstance(model._meta.pk, UUIDField)]
    
    # Iterate over UUID models to find the task with the given record ID
    for model in uuid_models:
        try:
            # Retrieve the task with the given record ID
            task = model.objects.filter(id=record_id).get()
            task_company = task.task_company
            
            # Generate a form dynamically for the task model
            TaskForm = modelform_factory(model, exclude=['user', 'date_opened', 'date_submitted', 'date_today', 'month_submit', 'task_company', 'is_completed', 'elapsed_time'])
            
            # Create an instance of the form with the task object
            form = TaskForm(request.POST or None, instance=task)
            
            # Set specific fields as read-only
            form.fields['name'].widget.attrs['readonly'] = True
            form.fields['client'].widget.attrs['readonly'] = True
            form.fields['task_segment'].widget.attrs['readonly'] = True
            
            # Break the loop since the task is found
            break
        except model.DoesNotExist:
            continue
    else:
        # If no task is found, display an error message and redirect to "index" view
        messages.success(request, 'Invalid Record ID!')
        return redirect('index')
     
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            is_paused = request.POST.get('is_paused')
            
            # Set the date_today field to the current date
            task.date_today = datetime.now().strftime('%Y%m%d') 
            
            # Set the month_submit field to the current month and year
            task.month_submit = datetime.now().strftime('%b-%Y')
            
            # Set the user field to the current user
            task.user = user
            
            # Calculate the elapsed time
            previous_elapsed_time = task.elapsed_time or timedelta(0)
            new_elapsed_time = request.POST.get('elapsed_time') or '0:0:0'
            new_elapsed_time = datetime.strptime(new_elapsed_time, '%H:%M:%S').time()
            new_elapsed_time_seconds = timedelta(hours=new_elapsed_time.hour, minutes=new_elapsed_time.minute, seconds=new_elapsed_time.second).total_seconds()
            task.elapsed_time = previous_elapsed_time + timedelta(seconds=new_elapsed_time_seconds)
            
            # Set the date_submitted field to the current date and time in the Manila timezone
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            
            if is_paused is None:
                # Check if any required fields are empty
                for field in form:
                    if not field.value():
                        form.add_error(field.name, f'{field.label} field is required.')
                
                # If there are form errors, return a JSON response with the errors
                if form.errors:
                    return JsonResponse({'success': False, 'errors': form.errors})
            
            if is_paused is not None:
                # If the task is being paused, update the is_completed field and save the task
                task.is_completed = False
                task.save()
                
                # Display a success message and redirect to "index" view
                messages.success(request, 'Task paused successfully!')
                return redirect('index')
            else:
                # If the task is being submitted as completed, update the is_completed field and save the task
                task.is_completed = True
                task.save()
                
                # Display a success message and return a JSON response with a redirect URL
                messages.success(request, 'Paused task submitted successfully!')
                return JsonResponse({'success': True, 'redirect_url': '/'})
            
    # Create a context dictionary with the form instance and other data
    context = {
        'form': form,
        'date_opened': request.session.get('date_opened', None),
        'company': task_company,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'id': record_id,
    }    
    
    # Render the "resume_tasks.html" template with the context
    return render(request, "resume_tasks.html", context)




def task_page(request):
    return render(request, 'task_page.html')
    


##----------------------------------------------##

## END USER VIEWS  @login_required decorator ##

##----------------------------------------------##


##################################################


##----------------------------------------------##

## TASKS FORM RENDERING AND SUBMISSION HANDLING - "ALL TASKS IN ALL APPS ARE THE SAME" ##

##----------------------------------------------##

## Declaring variable to store timezone formatting data ## 
manila_tz = pytz.timezone('Asia/Manila')

@login_required
def start_Categoryone_task(request):
    view = request.GET.get('view')    
    user = request.user
    logging.debug(print(request))

    # If there is a POST request, initialize the Categoryone and set elapsed_time to elapsed_time from the POST request
    if request.method == 'POST':
        form = CategoryoneForm(request.POST, elapsed_time=request.POST.get('elapsed_time'))
        is_paused = request.POST.get('is_paused')

        # If there are no form errors, set the form fields (task.<field>) to the following values
        if form.is_valid():
            task = form.save(commit=False)
            task.client = 'Form Category 2'
            task.task_company = 'Example Form 1' 
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date
            except ValueError:
                raise ValidationError('Invalid date format')
            # Set date_submitted to the current timezone-aware datetime
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.date_today = datetime.now().strftime('%Y%m%d') 
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            
            # If there is no data from request.POST, check for empty fields in the form
            if is_paused is None:
                for field in form:
                    if not field.value():
                        form.add_error(field.name, f'{field.label} field is required.')

                if form.errors:
                    return JsonResponse({'success': False, 'errors': form.errors})
                
            # If there is data from request.POST (is_paused), save the form data as a paused task
            if is_paused is not None:
                task.is_completed = False
                task.save()
                messages.success(request, 'Task paused successfully!')
                return redirect('index')
            else:
                # If there is no is_paused data, save the form data as a completed task
                task.is_completed = True
                task.save()
                messages.success(request, 'Task submitted successfully!')
                return JsonResponse({'success': True, 'redirect_url': '/'})
                
         
    # If it's not a POST request, render the form with initial values set to the user's first name and last name,
    # the task segment obtained from the GET request, and the current date and time for date_opened
    else:
        task_seg = request.GET.get('task_segment')
        user = request.user
        form = CategoryoneForm(initial={'name': f"{user.first_name} {user.last_name}", 'task_segment': task_seg})
        date_opened = request.session.get('date_opened', None) or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        request.session['date_opened'] = date_opened

    context = {
        'form': form,
        'date_opened': request.session['date_opened'],
        'task': 'Example Form 1',
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'view': view,
    }
    
    # Render the "start_task.html" template with the context
    return render(request, 'start_task.html', context)


@login_required
def start_Categoryone_task2(request):
    view = request.GET.get('view')    
    user = request.user
    if request.method == 'POST':
        form = CategoryoneForm2(request.POST, elapsed_time=request.POST.get('elapsed_time'))
        if form.is_valid():
            task = form.save(commit=False)
            task.client = 'Form Category 2'
            task.task_company = 'Example Form 2'
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date
            except ValueError:
                raise ValidationError('Invalid date format')
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.date_today = datetime.now().strftime('%Y%m%d') 
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            is_paused = request.POST.get('is_paused')
            if is_paused is None:
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
        form = CategoryoneForm2(initial={'name':f"{user.first_name} {user.last_name}",'task_segment': task_seg})
        request.session['date_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    context = {
        'form': form,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'task': 'Example Form 2',
        'date_opened': request.session.get('date_opened', None),
        'view': view,
    }
    return render(request, 'start_task.html', context)


@login_required
def start_Categoryone_task3(request):
    view = request.GET.get('view')    
    user = request.user
    if request.method == 'POST':
        form = CategoryoneForm3(request.POST, elapsed_time=request.POST.get('elapsed_time'))
        if form.is_valid():
            task = form.save(commit=False)
            task.client = 'Form Category 2'
            task.task_company = 'Example Form 3'
            date_opened = request.POST.get('date_opened')
            try:
                parsed_date = datetime.strptime(date_opened, '%Y-%m-%dT%H:%M:%S.%fZ')
                formatted_date = parsed_date + timedelta(hours=8)
                formatted_date_str = formatted_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date_str
            except:
                parsed_date = datetime.strptime(date_opened, '%m/%d/%Y, %I:%M:%S %p')
                formatted_date = parsed_date + timedelta(hours=8)
                formatted_date_str = formatted_date.strftime('%Y-%m-%d %H:%M:%S')
                task.date_opened = formatted_date_str
                
            date_submitted = timezone.now().astimezone(manila_tz)
            task.date_submitted = date_submitted
            task.date_today = datetime.now().strftime('%Y%m%d')
            task.month_submit = datetime.now().strftime('%b-%Y')
            task.user = user
            is_paused = request.POST.get('is_paused')
            if is_paused is None:
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
        form = CategoryoneForm3(initial={'name':f"{user.first_name} {user.last_name}",'task_segment': task_seg})
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(time)
        
    
    context = {
        'form': form,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'task': 'Example Form 3',
        'date_opened': time,
        'view': view
    }
    return render(request, 'start_task.html', context)

##----------------------------------------------##

## END TASKS FORM RENDERING AND SUBMISSION HANDLING ##

##----------------------------------------------##