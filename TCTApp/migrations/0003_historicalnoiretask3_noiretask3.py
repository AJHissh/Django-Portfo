# Generated by Django 5.0.6 on 2024-05-13 00:18

import TCTApp.models
import datetime
import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TCTApp', '0002_remove_historicalnoiretask11_history_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalNoireTask3',
            fields=[
                ('name', models.CharField(db_index=True, max_length=100)),
                ('date_opened', models.DateTimeField(db_index=True, null=True)),
                ('date_submitted', models.DateTimeField(db_index=True, null=True)),
                ('elapsed_time', models.DurationField(default=datetime.timedelta(0))),
                ('date_today', models.CharField(default='None', max_length=100, null=True)),
                ('month_submit', models.CharField(default='None', max_length=100, null=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('client', models.CharField(db_index=True, default='Category 2', max_length=100)),
                ('task_segment', models.CharField(default='None', max_length=100)),
                ('task_company', models.CharField(max_length=100)),
                ('is_completed', models.BooleanField(db_index=True, default=False)),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='Company name')),
                ('question_1', models.CharField(blank=True, max_length=100, verbose_name='Application Tracking Number')),
                ('question_2', models.CharField(blank=True, max_length=100, verbose_name='MCC / Merchant Industry')),
                ('question_3', models.CharField(blank=True, choices=[('Others', 'Others'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Belgium', 'Belgium'), ('Bulgaria', 'Bulgaria'), ('Others', 'Others'), ('Canada', 'Canada'), ('Canada (Quebec)', 'Canada (Quebec)'), ('Croatia', 'Croatia'), ('Cyprus', 'Cyprus'), ('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark'), ('Estonia', 'Estonia'), ('Finland', 'Finland'), ('France', 'France'), ('Germany', 'Germany'), ('Greece', 'Greece'), ('Gurnsey', 'Gurnsey'), ('Hong Kong', 'Hong Kong'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jersey', 'Jersey'), ('Latvia', 'Latvia'), ('Liechtenstein', 'Liechtenstein'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Malta', 'Malta'), ('Netherlands', 'Netherlands'), ('New Zealand', 'New Zealand'), ('Norway', 'Norway'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Romania', 'Romania'), ('Serbia', 'Serbia'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia'), ('Spain', 'Spain'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('United Kingdom', 'United Kingdom'), ('Quebec', 'Quebec')], max_length=100, verbose_name='Country of Incorporation')),
                ('question_4', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=100, verbose_name='Is this your first review?')),
                ('question_5', models.CharField(blank=True, max_length=100, verbose_name=' Accomplished Merchant Application Form')),
                ('question_6', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Identification - How many IDs reviewed?')),
                ('question_7', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name='Proof of Identification - How many IDs are VALID?')),
                ('question_8', models.CharField(blank=True, max_length=100, verbose_name='Whos IDs do they belong to')),
                ('question_9', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills reviewed?')),
                ('question_10', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills are VALID?')),
                ('question_11', models.CharField(blank=True, max_length=100, verbose_name='Whos POAs do these belong to?')),
                ('question_12', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Certificate of Incorporation')),
                ('question_13', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Trade Register Excerpt (Company Registration)')),
                ('question_14', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Documents shwing list of Directors, Managers, and Shareholders')),
                ('question_15', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Card Processing History')),
                ('question_16', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide'), ('Business License (If Applicable)', 'Business License (If Applicable)')], max_length=100, verbose_name='Business License (If Applicable)')),
                ('question_17', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='6 months of corporate bank statements & a voided cheque')),
                ('question_18', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Proof of Operating Address (Lease Agreement, Corporate Bank Statement or Corporate Utility Bill issued within 90 days)')),
                ('question_19', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Proof of domaion ownership')),
                ('question_20', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Required but did not provide', 'Required but did not provide'), ('Did Not Provide', 'Did Not Provide'), ('Not Applicable', 'Not Applicable')], max_length=100, verbose_name='if PCI-DSS compliant, please submit a PCI-DSS certificate')),
                ('question_21', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Required but did not provide', 'Required but did not provide'), ('Did Not Provide', 'Did Not Provide'), ('Not Applicable', 'Not Applicable')], max_length=100, verbose_name='AML Policy/Terms and Conditions (if applicable)')),
                ('question_22', models.CharField(blank=True, max_length=100, verbose_name='OTHER (list the documents - separate with a semi-colon[;] and identify if VALID ie. Rental Agreement(Valid), Gaming License(Valid))')),
                ('question_23', models.TextField(blank=True, max_length=750, verbose_name='Comments')),
                ('question_24', models.CharField(blank=True, choices=[('Validation: Continue Review (of Tasks)', 'Validation: Continue Review (of Tasks)'), ('Escalate to Client', 'Escalate to Client'), ('Communicate findings to Merchant / Pend - Internal Review', 'Communicate findings to Merchant / Pend - Internal Review'), ('Pend - Internal Review', 'Pend - Internal Review'), ('For Quality Check', 'For Quality Check'), ('For Client Quality Checking', 'Escalate to Client'), ('For Approval', 'For Approval'), ('For Rejection/Pend', 'For Rejection/Pend'), ('For Follow-up', 'For Follow-up')], max_length=100, verbose_name='Next Tasks / Steps')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, to_field='uuid')),
            ],
            options={
                'verbose_name': 'historical noire task3',
                'verbose_name_plural': 'historical noire task3s',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='NoireTask3',
            fields=[
                ('name', models.CharField(db_index=True, max_length=100)),
                ('date_opened', models.DateTimeField(db_index=True, null=True)),
                ('date_submitted', models.DateTimeField(db_index=True, null=True)),
                ('elapsed_time', models.DurationField(default=datetime.timedelta(0))),
                ('date_today', models.CharField(default='None', max_length=100, null=True)),
                ('month_submit', models.CharField(default='None', max_length=100, null=True)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('client', models.CharField(db_index=True, default='Category 2', max_length=100)),
                ('task_segment', models.CharField(default='None', max_length=100)),
                ('task_company', models.CharField(max_length=100)),
                ('is_completed', models.BooleanField(db_index=True, default=False)),
                ('company', models.CharField(blank=True, max_length=100, verbose_name='Company name')),
                ('question_1', models.CharField(blank=True, max_length=100, verbose_name='Application Tracking Number')),
                ('question_2', models.CharField(blank=True, max_length=100, verbose_name='MCC / Merchant Industry')),
                ('question_3', models.CharField(blank=True, choices=[('Others', 'Others'), ('Australia', 'Australia'), ('Austria', 'Austria'), ('Belgium', 'Belgium'), ('Bulgaria', 'Bulgaria'), ('Others', 'Others'), ('Canada', 'Canada'), ('Canada (Quebec)', 'Canada (Quebec)'), ('Croatia', 'Croatia'), ('Cyprus', 'Cyprus'), ('Czech Republic', 'Czech Republic'), ('Denmark', 'Denmark'), ('Estonia', 'Estonia'), ('Finland', 'Finland'), ('France', 'France'), ('Germany', 'Germany'), ('Greece', 'Greece'), ('Gurnsey', 'Gurnsey'), ('Hong Kong', 'Hong Kong'), ('Hungary', 'Hungary'), ('Iceland', 'Iceland'), ('Ireland', 'Ireland'), ('Isle of Man', 'Isle of Man'), ('Israel', 'Israel'), ('Italy', 'Italy'), ('Jersey', 'Jersey'), ('Latvia', 'Latvia'), ('Liechtenstein', 'Liechtenstein'), ('Lithuania', 'Lithuania'), ('Luxembourg', 'Luxembourg'), ('Malta', 'Malta'), ('Netherlands', 'Netherlands'), ('New Zealand', 'New Zealand'), ('Norway', 'Norway'), ('Poland', 'Poland'), ('Portugal', 'Portugal'), ('Romania', 'Romania'), ('Serbia', 'Serbia'), ('Singapore', 'Singapore'), ('Slovakia', 'Slovakia'), ('Spain', 'Spain'), ('Sweden', 'Sweden'), ('Switzerland', 'Switzerland'), ('United Kingdom', 'United Kingdom'), ('Quebec', 'Quebec')], max_length=100, verbose_name='Country of Incorporation')),
                ('question_4', models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No')], max_length=100, verbose_name='Is this your first review?')),
                ('question_5', models.CharField(blank=True, max_length=100, verbose_name=' Accomplished Merchant Application Form')),
                ('question_6', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Identification - How many IDs reviewed?')),
                ('question_7', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name='Proof of Identification - How many IDs are VALID?')),
                ('question_8', models.CharField(blank=True, max_length=100, verbose_name='Whos IDs do they belong to')),
                ('question_9', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills reviewed?')),
                ('question_10', models.IntegerField(blank=True, null=True, validators=[TCTApp.models.number_range], verbose_name=' Proof of Address (Utility Bills) - How many Utility Bills are VALID?')),
                ('question_11', models.CharField(blank=True, max_length=100, verbose_name='Whos POAs do these belong to?')),
                ('question_12', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Certificate of Incorporation')),
                ('question_13', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Trade Register Excerpt (Company Registration)')),
                ('question_14', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did not provide but downloaded from registry', 'Did not provide but downloaded from registry'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='KYB - Documents shwing list of Directors, Managers, and Shareholders')),
                ('question_15', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Card Processing History')),
                ('question_16', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide'), ('Business License (If Applicable)', 'Business License (If Applicable)')], max_length=100, verbose_name='Business License (If Applicable)')),
                ('question_17', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='6 months of corporate bank statements & a voided cheque')),
                ('question_18', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Proof of Operating Address (Lease Agreement, Corporate Bank Statement or Corporate Utility Bill issued within 90 days)')),
                ('question_19', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Did Not Provide', 'Did Not Provide')], max_length=100, verbose_name='Proof of domaion ownership')),
                ('question_20', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Required but did not provide', 'Required but did not provide'), ('Did Not Provide', 'Did Not Provide'), ('Not Applicable', 'Not Applicable')], max_length=100, verbose_name='if PCI-DSS compliant, please submit a PCI-DSS certificate')),
                ('question_21', models.CharField(blank=True, choices=[('Provided - Complete and Valid', 'Provided - Complete and Valid'), ('Provided - Incomplete / Invalid', 'Provided - Incomplete / Invalid'), ('Required but did not provide', 'Required but did not provide'), ('Did Not Provide', 'Did Not Provide'), ('Not Applicable', 'Not Applicable')], max_length=100, verbose_name='AML Policy/Terms and Conditions (if applicable)')),
                ('question_22', models.CharField(blank=True, max_length=100, verbose_name='OTHER (list the documents - separate with a semi-colon[;] and identify if VALID ie. Rental Agreement(Valid), Gaming License(Valid))')),
                ('question_23', models.TextField(blank=True, max_length=750, verbose_name='Comments')),
                ('question_24', models.CharField(blank=True, choices=[('Validation: Continue Review (of Tasks)', 'Validation: Continue Review (of Tasks)'), ('Escalate to Client', 'Escalate to Client'), ('Communicate findings to Merchant / Pend - Internal Review', 'Communicate findings to Merchant / Pend - Internal Review'), ('Pend - Internal Review', 'Pend - Internal Review'), ('For Quality Check', 'For Quality Check'), ('For Client Quality Checking', 'Escalate to Client'), ('For Approval', 'For Approval'), ('For Rejection/Pend', 'For Rejection/Pend'), ('For Follow-up', 'For Follow-up')], max_length=100, verbose_name='Next Tasks / Steps')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='uuid')),
            ],
        ),
    ]
