from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime
from django.contrib.auth import get_user_model
import uuid
from simple_history.models import HistoricalRecords


## choices ##

diff_choices = [
    ('simple', 'Simple'),
    ('complex', 'Complex'),
    ]

radiobutton1_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ]

radiobutton2_choices = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ('n/a', 'N/A')
    ]

media_choices = [
    ('Google', 'Google'),
    ('Facebook', 'Facebook'),
    ('LinkedIn', 'LinkedIn'),
    ('Others', 'Others'),
    ]


risk_choices = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Restriced', 'Restricted'),
    ('Prohibited', 'Prohibited'),
    ]




## END WIDGETS ##

User = get_user_model()

class Categorytwo(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category One', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    company = models.CharField(max_length=100, blank=True)
    question_1 = models.CharField(max_length=100, blank=True, verbose_name='Level of Risk?', choices=risk_choices)
    question_2 = models.CharField(max_length=100, blank=True, verbose_name='E-mail Address')
    question_3 = models.CharField(max_length=100, blank=True, verbose_name='Role')
    question_4 = models.CharField(max_length=100, blank=True,  verbose_name='Social Media Site', choices=media_choices)
    question_5 = models.TextField(max_length=750, verbose_name='Comments', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)

class Categorytwo2(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category One', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    question_1 = models.CharField(max_length=100, blank=True, verbose_name='Application ID')
    question_2 = models.CharField(max_length=100, blank=True, verbose_name='Company Name')
    question_3 = models.IntegerField(verbose_name='Number of Users you will be assigning', blank=True, null=True)
    question_4 = models.TextField(max_length=500, blank=True,  verbose_name='Who are assigned (If multiple COT users, please seperate with a semi-colon (;))')
    question_5 = models.TextField(max_length=750, blank=True, verbose_name='Comments')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)

class Categorytwo3(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='uuid')
    date_opened = models.DateTimeField(null=True, db_index=True)
    date_submitted = models.DateTimeField(null=True, db_index=True)
    elapsed_time = models.DurationField(default=datetime.timedelta())
    date_today = models.CharField(max_length=100,null=True, default='None')
    month_submit = models.CharField(null=True, default='None', max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    client = models.CharField(max_length=100, default='Category One', db_index=True)
    task_segment = models.CharField(max_length=100, default='None')
    task_company = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False, db_index=True)
    history = HistoricalRecords()
    question_1 = models.CharField(max_length=100, blank=True, verbose_name='Application ID')
    question_2 = models.CharField(max_length=100, blank=True, verbose_name='Company Name')
    question_3 = models.CharField(max_length=100, blank=True, verbose_name='EMAIL of COT User Assigned to this Application')
    question_4 = models.TextField(max_length=750, blank=True, verbose_name='Comments')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            user_model = get_user_model()
            user = user_model.objects.get(email=self.email)
        super().save(*args, **kwargs)
