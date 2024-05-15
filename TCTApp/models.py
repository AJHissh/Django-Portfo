from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth import get_user_model
import uuid
from simple_history.models import HistoricalRecords
import random
import string


##----------------------------------------------##

## Create list of tuples to be used for radio button choices and list choices ##

##----------------------------------------------##

radiobutton1_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ]

doc_submitted = [
     ('Provided - Complete and Valid', 'Provided - Complete and Valid'),
     ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'),
     ('Did Not Provide', 'Did Not Provide'),  
]

doc_submitted_bus_lic = [
     ('Provided - Complete and Valid', 'Provided - Complete and Valid'),
     ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'),
     ('Did Not Provide', 'Did Not Provide'),
     ('Business License (If Applicable)', 'Business License (If Applicable)')  
]


doc_submitted2 = [
     ('Provided - Complete and Valid', 'Provided - Complete and Valid'),
     ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'),
     ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'),
     ('Did Not Provide', 'Did Not Provide'),  
]

doc_submitted3 = [
     ('Provided - Complete and Valid', 'Provided - Complete and Valid'),
     ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'),
     ('Required but did not provide', 'Required but did not provide'),
     ('Did Not Provide', 'Did Not Provide'),
     ('Not Applicable', 'Not Applicable'),    
]

nextstep_choices= [
    ('Validation: Continue Review (of Tasks)', 'Validation: Continue Review (of Tasks)'),
    ('Escalate to Client', 'Escalate to Client'),
    ('Communicate findings to Merchant / Pend - Internal Review', 'Communicate findings to Merchant / Pend - Internal Review'),
    ('Pend - Internal Review', 'Pend - Internal Review'),
    ('For Quality Check', 'For Quality Check'),
    ('For Client Quality Checking', 'Escalate to Client'),
    ('For Approval', 'For Approval'),
    ('For Rejection/Pend', 'For Rejection/Pend'),
    ('For Follow-up', 'For Follow-up'),
    ]

nextstep_choices2= [
    ('Validation: Continue Review (of Tasks)', 'Validation: Continue Review (of Tasks)'),
    ('Escalate to Client', 'Escalate to Client'),
    ('Communicate findings to Merchant / Pend - Internal Review', 'Communicate findings to Merchant / Pend - Internal Review'),
    ('Pend - Internal Review', 'Pend - Internal Review'),
    ('For Quality Check', 'For Quality Check'),
    ('For Client Quality Checking', 'Escalate to Client'),
    ('For Approval', 'For Approval'),
    ('For Rejection/Pend', 'For Rejection/Pend'),
    ('Not Applicable (Not merchant related)', 'Not Applicable (Not merchant related)'),
    ]


acquirers = [
    ('Credorax / Finaro', 'Credorax / Finaro'),
    ('ECP', 'ECP'),
    ('Cashflows', 'Cashflows'),
    ('Safecharge', 'Safecharge'),
    ('Concardis', 'Concardis'),
    ('Paysafe', 'Paysafe'),
    ('Bank Frick', 'Bank Frick'),
    ('Decta', 'Decta'),
    ('Paydoo', 'Paydoo'),
    ('Ecommpay', 'Ecommpay'),
    ('Secure Trading / Acquiring.com / Trust Payments', 'Secure Trading / Acquiring.com / Trust Payments'),
    ('Others', 'Others'),
    ]


country_choices  = [
    ('Others', 'Others'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Belgium', 'Belgium'),
    ('Bulgaria', 'Bulgaria'),
    ('Others', 'Others'),
    ('Canada', 'Canada'),
    ('Canada (Quebec)', 'Canada (Quebec)'),
    ('Croatia', 'Croatia'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Denmark', 'Denmark'),
    ('Estonia', 'Estonia'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('Germany', 'Germany'),
    ('Greece', 'Greece'),
    ('Gurnsey', 'Gurnsey'),
    ('Hong Kong', 'Hong Kong'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('Ireland', 'Ireland'),
    ('Isle of Man', 'Isle of Man'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Jersey', 'Jersey'),
    ('Latvia', 'Latvia'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Malta', 'Malta'),
    ('Netherlands', 'Netherlands'),
    ('New Zealand', 'New Zealand'),
    ('Norway', 'Norway'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Romania', 'Romania'),
    ('Serbia', 'Serbia'),
    ('Singapore', 'Singapore'),
    ('Slovakia', 'Slovakia'),
    ('Spain', 'Spain'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('United Kingdom', 'United Kingdom'),
    ('Quebec', 'Quebec'),
]
##----------------------------------------------##

## END Create list of tuples to be used for radio button choices and list choices ##

##----------------------------------------------##

##################################################

##----------------------------------------------##

## Models for App 1 ##

##----------------------------------------------##


## This is a function used for data validation that requires a number between 0 and 50 ## 
def number_range(value):
    if value is not None and (value < 0 or value > 50):
        raise ValidationError(
            _(f"{value} is not a valid number. Please enter a number between 0 and 50."),
            code='invalid_number_range'
        )

## This is the model for a user who creates an account ## 
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pass


class GuestUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)

    @classmethod
    def create_guest_user(cls, username, password, first_name, last_name, email):
        # Create a new user with the provided username and password
        user = User.objects.create_user(username=username, password=password)
        
        # Create a GuestUser object associated with the newly created user
        return cls.objects.create(user=user, first_name=first_name, last_name=last_name, email=email)


## Request Edit model for data inputted into the request edit form ## 
class RequestEdit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=100, db_index=True, default='None')
    history = HistoricalRecords()
    record_ID = models.CharField(max_length=255, default='None')
    change = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, default='None')
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    
class Categoryone(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category 2', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    company = models.CharField(max_length=100,blank=True, verbose_name='Company name')
    question_1 = models.CharField(max_length=100,blank=True, verbose_name='Merchant Reference Number')
    question_2 = models.TextField(max_length=750, verbose_name='Comments (If Any)', blank=True, null=True)
    question_3 = models.CharField(max_length=100,blank=True, verbose_name='Next Tasks/Steps',choices=nextstep_choices2)    

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)
        
    
 
class Categoryone2(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category 2', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    company = models.CharField(max_length=100, blank=True, verbose_name='Company name')
    question_1 = models.CharField(max_length=100, blank=True,verbose_name='Which Acquirer will this be submitted to?', choices=acquirers) 
    question_2 = models.CharField(max_length=100, verbose_name='If Others - Please Specify', blank=True, null=True)
    question_3 = models.CharField(max_length=100, blank=True, verbose_name='MCC / Merchant Industry')
    question_4 = models.CharField(max_length=100, blank=True, verbose_name='Monthly Sales Volume')
    question_5 = models.CharField(max_length=100, blank=True, verbose_name='Did you manually fill in information in the acquirers portal / application form as part of this proccess? If Yes, please identify how extensive the effort was.', choices=[('no', 'No'), ('Not_Extensive', 'Not Extensive (3 - 10 fields)'), ('Somewhat_Extensive', 'Somewhat Extensive (11-20 fields)'),('Extensive', 'Extensive (More than 20 fields)')])
    question_6 = models.IntegerField(validators=[number_range],verbose_name='If No, please specify how many times you have submitted this merchant for Pre-approval.', blank=True, null=True)
    question_7 = models.TextField(max_length=750, blank=True, verbose_name='Comment/s:', null=True)
    question_8 = models.CharField(max_length=100, blank=True, verbose_name='Next Tasks/Steps',choices=nextstep_choices2)    

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)
        
class Categoryone3(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category 2', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    company = models.CharField(max_length=100, blank=True, verbose_name='Company name')
    question_1 = models.CharField(max_length=100, blank=True, verbose_name='Application Tracking Number')
    question_2 = models.CharField(max_length=100, blank=True, verbose_name='MCC / Merchant Industry')
    question_3 = models.CharField(max_length=100, blank=True, verbose_name='Country of Incorporation', choices=country_choices)
    question_4 = models.CharField(max_length=100, blank=True, verbose_name='Is this your first review?', choices=radiobutton1_choices)
    question_5 = models.CharField(max_length=100, blank=True, verbose_name=' Accomplished Merchant Application Form')
    question_6 = models.IntegerField(blank=True, null=True, validators=[number_range], verbose_name=' Proof of Identification - How many IDs reviewed?')
    question_7 = models.IntegerField( blank=True, null=True, validators=[number_range], verbose_name='Proof of Identification - How many IDs are VALID?')
    question_8 = models.CharField(max_length=100, blank=True, verbose_name='Whos IDs do they belong to')
    question_9 = models.IntegerField( blank=True, null=True, validators=[number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills reviewed?')
    question_10 = models.IntegerField( blank=True, null=True, validators=[number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills are VALID?')
    question_11 = models.CharField(max_length=100, blank=True, verbose_name='Whos POAs do these belong to?')
    question_12 = models.CharField(max_length=100, blank=True, choices=doc_submitted2, verbose_name='KYB - Certificate of Incorporation')
    question_13 = models.CharField(max_length=100, blank=True, choices=doc_submitted2, verbose_name='KYB - Trade Register Excerpt (Company Registration)')
    question_14 = models.CharField(max_length=100, blank=True, choices=doc_submitted2, verbose_name='KYB - Documents shwing list of Directors, Managers, and Shareholders')
    question_15 = models.CharField(max_length=100, blank=True, choices=doc_submitted, verbose_name='Card Processing History')
    question_16 = models.CharField(max_length=100, blank=True, choices=doc_submitted_bus_lic,verbose_name='Business License (If Applicable)')
    question_17 = models.CharField(max_length=100, blank=True, choices=doc_submitted, verbose_name='6 months of corporate bank statements & a voided cheque')
    question_18 = models.CharField(max_length=100, blank=True, choices=doc_submitted, verbose_name='Proof of Operating Address (Lease Agreement, Corporate Bank Statement or Corporate Utility Bill issued within 90 days)')
    question_19 = models.CharField(max_length=100, blank=True, choices=doc_submitted, verbose_name='Proof of domaion ownership')
    question_20 = models.CharField(max_length=100, blank=True, choices=doc_submitted3, verbose_name='if PCI-DSS compliant, please submit a PCI-DSS certificate')    
    question_21 = models.CharField(max_length=100, blank=True, choices=doc_submitted3, verbose_name='AML Policy/Terms and Conditions (if applicable)')
    question_22 = models.CharField(max_length=100, blank=True, verbose_name='OTHER (list the documents - separate with a semi-colon[;] and identify if VALID ie. Rental Agreement(Valid), Gaming License(Valid))')    
    question_23 = models.TextField(max_length=750, blank=True, verbose_name='Comments')    
    question_24 = models.CharField(max_length=100, blank=True, choices=nextstep_choices,verbose_name='Next Tasks / Steps')               

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)
        
        
        
##----------------------------------------------##

## END Models for App 1 ##

##----------------------------------------------##