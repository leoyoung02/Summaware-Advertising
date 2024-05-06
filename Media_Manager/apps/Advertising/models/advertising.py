from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.forms import model_to_dict

from datetime import datetime, date

from django.http import JsonResponse

# ------- MODEL DEFINITIONS -------
class SalesPerson(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default=None)
    address = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=100, default=None)
    state = models.CharField(max_length=100, default=None)
    zip_code = models.CharField(max_length=100, default=None)
    email = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=100, null=True, default=None)
    active = models.BooleanField(default=True)
    commission_percentage = models.FloatField(default=0.0)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'advertising_salesperson'

class IndustryCode(models.Model):
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    account = models.ForeignKey('Account', on_delete=CASCADE)

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_industrycode'

class CompanyDepartment(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'advertising_department'

class Account(models.Model):
    submitter = models.CharField(max_length=100)
    account_type = models.ForeignKey('AccountType', null=True, on_delete=SET_NULL)
    sales_person = models.ForeignKey('SalesPerson', null=True, on_delete=SET_NULL, default=None)
    industry_code = models.ForeignKey('IndustryCode', null=True, on_delete=SET_NULL, default=None, related_name='account_industry_code')
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=255)

    # it is extra fields added by Chase - start
    contact_name_first = models.CharField(max_length=100)
    contact_name_last = models.CharField(max_length=100)
    company_name_1 = models.CharField(max_length=255)
    company_name_2 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    tearsheets = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50)
    prepay_required = models.BooleanField(default=False)
    # it is extra fields added by Chase - end
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    website = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True)
    archived = models.BooleanField(default=False)
    legacy_id = models.CharField(max_length=100, default=None, null=True, blank=True)
    balance = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    total_spent = models.FloatField(default=0.00)
    last_activity = models.CharField(max_length=100)
    last_ad_run = models.DateField(default=None)
    can_run_ads = models.BooleanField(default=True)
    default_publication = models.ForeignKey('Publication', on_delete=SET_NULL, null=True, default=None)
    can_accept_checks = models.BooleanField(default=True)
    tax_exempt = models.BooleanField(default=False)
    last_payment_date = models.CharField(max_length=100)
    invoice_frequency = models.CharField(default='period', max_length=45)
    invoice_type = models.CharField(default='email', max_length=45)
    mail_invoice_charge = models.FloatField(default=0.00)
    credit = models.DecimalField(default=0, max_digits=19, decimal_places=2)
    credit_limit = models.DecimalField(default=1000.0, max_digits=19, decimal_places=2)
    write_off_amount = models.IntegerField(default=0)
    write_off_period  = models.CharField(max_length=30, default=None)
    # use_credit_first = models.BooleanField(default=True)
    prepay_required = models.BooleanField(default=False)
    billing_email = models.EmailField(max_length=100)
    billing_address = models.EmailField(max_length=100)
    billing_city = models.EmailField(max_length=100)
    billing_state = models.EmailField(max_length=100)
    billing_zip_code = models.EmailField(max_length=100)
    status = models.IntegerField(default=0)
    # TODO - add a field for logo image
    # TODO - add a field for secondary legacy id (will be exactly like the first legacy id)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_account_notes', 'Can view account notes'),
            ('can_view_sales_rep_notes', 'Can view sales rep notes'),
            ('can_add_sales_rep_notes', 'Can add sales rep notes'),
            # TODO - add permission to restrict access to changing sales rep field
        )
        db_table = 'advertising_account'

class AccountAddress(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, default=None)
    address1 = models.CharField(max_length=255, default=None)
    address2 = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=255, default=None)
    state = models.CharField(max_length=50, default=None)
    zip_code = models.CharField(max_length=50)
    primary = models.BooleanField(default=False)
    billing = models.BooleanField(default=False)

    class Meta:
        db_table = 'advertising_accountaddress'
    
class AccountType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'advertising_accounttype'

class MarketCode(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    active = models.IntegerField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

    class Meta:
        db_table = "advertising_marketcode"

class CompanyContact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=CASCADE)
    department = models.ForeignKey('CompanyDepartment', on_delete=CASCADE)
    default = models.IntegerField()
    active = models.IntegerField()
    class Meta:
        db_table = 'advertising_companycontact'

class AdvertiserTaskList(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    due_date = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    note = models.CharField(max_length=100)
    account = models.ForeignKey('Account', on_delete=CASCADE)
    status = models.IntegerField()
    complete = models.IntegerField()
    class Meta:
        db_table = 'advertising_tasks'

class AccountHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    detail = models.CharField(max_length=100)
    submitter = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_accounthistory'

class AccountPaymentHistory(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    amount = models.FloatField()
    payment_type = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True, null=True)
    payment_method = models.CharField(max_length=100)
    payment_notes = models.TextField(null=True)

    class Meta:
        db_table = 'advertising_accountpaymenthistory'

# TODO - Add a model for company contacts history

class Adjustment(models.Model):
    code = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=255, default=None)
    apply_level = models.CharField(max_length=50) # ['order', 'insertion']
    value_type = models.CharField(max_length=50) # ['amount', 'percentage']
    amount = models.FloatField(default=0.00)
    date_created = models.DateTimeField(auto_now=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.CharField(max_length=100) # username
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE)
    type = models.CharField(max_length=20) # ['credit', 'debit']
    # type = models.CharField(max_length=20) # ['gross', 'net']
    active = models.BooleanField(default=True)    
    prompt_for_value = models.BooleanField(default=False)
    section = models.ForeignKey('PublicationSection', on_delete=models.CASCADE, default=None)
    # gross_net = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'advertising_adjustment'

    def __str__(self):
        return self.code

class AccountNote(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    note = models.TextField(null=True)
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_accountnote'

class AccountSalesRepNote(models.Model):
    account = models.ForeignKey('Account', on_delete=CASCADE)
    sales_person = models.ForeignKey(SalesPerson, on_delete=CASCADE)
    note = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'advertising_accountsalesrepnote'

class SalesPersonTask(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(null=True, default=datetime.today().strftime('%Y/%m/%d'))
    salesperson = models.ForeignKey('SalesPerson', on_delete=CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'advertising_salespersontask'

class SalesPersonLedger(models.Model):
    salesperson = models.ForeignKey('SalesPerson', on_delete=CASCADE)
    order = models.ForeignKey('AdvertisingOrder', on_delete=CASCADE)
    money_spent = models.FloatField(default=0.0)
    date_spent = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'advertising_salespersonledger'

class SubCompany(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Example --> region, subsection, dept., etc.

    class Meta:
        db_table = 'advertising_subcompany'

# ------- MODEL METHODS -------
def getSalesPersonFullName(salesrep_id):
    """
        @param salesrep_id: the id of a salesperson

        returns the full name of a salesperson
    """

    try:
        salesrep = SalesPerson.objects.get(id=salesrep_id)
    except SalesPerson.DoesNotExist:
        return ""
    
    return str(salesrep.first_name + " " + salesrep.last_name)

def getActiveSalesPersonTasks(salesrep):
    """
        @param salesrep: a SalesPerson object

        returns an array of dictionaries containing the salesperson's active tasks
    """
    return [model_to_dict(task) for task in SalesPersonTask.objects.filter(salesperson=salesrep, completed=False)]

def getOverdueSalesPersonTasks(salesrep):
    """
        @param salesrep: a SalesPerson object

        returns an array of dictionaries containing the salesperson's overdue tasks
    """
    overdue_tasks = []
    try:
        taskList = SalesPersonTask.objects.filter(salesperson=salesrep)
        if taskList:
            for task in taskList:
                if task.date < datetime.date(datetime.today()) and not task.completed:
                    overdue_tasks.append(model_to_dict(task))

        else:
            return []
        return overdue_tasks
    except SalesPersonTask.DoesNotExist:
        return []

def wasCreatedRecently(account):
    """
        @param account: an instance of the Account model

        returns True if account.created_at was less than a month ago and False if otherwise
    """

    return (date.today() - account.created_at.date()).days < 30
   