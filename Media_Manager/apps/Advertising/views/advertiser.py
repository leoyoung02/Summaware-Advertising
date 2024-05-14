from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)

import json
from django.shortcuts import render
from ..models.advertising import *
from ..models.classifieds import *
from ..models.advertising import Account, SalesPerson, AccountType, MarketCode, IndustryCode, CompanyContact, AdvertiserTaskList
from .... import views
from ..forms import *
from django.core import serializers

login_redirect = "/login/?next="

daysOfTheWeek = ['monday', 'tuesday', 'wednesday',
                     'thursday', 'friday', 'saturday', 'sunday']

def advertiser_dashboard(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'GET':
        advertiserId = request.GET.get('advertiserId')

    newAccount = Account.objects.get(id=advertiserId)
    accountTypes = AccountType.objects.all()
    accountTypeList = serializers.serialize('json', accountTypes)
    department = CompanyDepartment.objects.all()
    accountInfo = Account.objects.all()
    adCampaign = ClassifiedCampaignSummary.objects.filter(advertiser_id=advertiserId)

    context = {
        "id": advertiserId,
        "newAccount": newAccount,
        "accountTypes": accountTypes,
        "accountTypeList": accountTypeList,
        "department": department,
        "accountInfo": accountInfo,
        "adCampaigns" : adCampaign
    }

    return render(request, "dashboard.html", context)

def advertiser_home(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "advertising")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    
    if request.method == 'GET':
        AccountList = Account.objects.select_related('account_type').all()
        context = {
            "accountList" : AccountList
        }
        return render(request, "HomeAdvertiser.html", context)

def edit_new_advertiser(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        row = Account.objects.get(id=data['id'])

        if data['param'] == 'walmart':
            row.status = data['status']
            row.address = data['address']
            row.website = data['website']
            row.account_type_id = data['accountType']
            row.phone = data['phone']
            row.email = data['email']
            row.save()

            return JsonResponse({"data": data}, status=200)

        if data['param'] == 'billing':
            row.total_spent = data['billing_total_spent']
            row.billing_address = data['billing_address']
            row.credit_limit = data['credit_limit']
            row.billing_email = data['billing_email']
            row.save()

            return JsonResponse({"data": data}, status=200)

def taskSetActivity(request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        row = AdvertiserTaskList.objects.get(id=data['id'])
        row.complete = 1
        row.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def create_task (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        if data['id'] == 0:
            task = AdvertiserTaskList(
                id = 1,
                title=data['title'],
                due_date=data['due_date'],
                priority=data['priority'],
                content=data['content'],
                account_id=data['account_id'],
                note=data['note'],
                complete=0,
                status=1
            )

            task.save()

        if data['id'] != 0:
            row = AdvertiserTaskList.objects.get(id=data['id'])

            row.title = data['title']
            row.due_date = data['due_date']
            row.priority = data['priority']
            row.account_id = data['account_id']
            row.content = data['content']
            row.note = data['note']

            row.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def delete_id_contact (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        obj_to_delete = CompanyContact.objects.get(id=data['id'])

        obj_to_delete.active = 0
        obj_to_delete.save()
        active_contacts = CompanyContact.objects.filter(active=1)
        ac_con = list(active_contacts.values())

        inactive_contacts = CompanyContact.objects.filter(active=0)
        inac_con = list(inactive_contacts.values())

        contacts = {
            'active': ac_con,
            'inactive': inac_con,
        }

        return JsonResponse(contacts)
def taskRemove (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        obj_to_delete = AdvertiserTaskList.objects.get(id=data['id'])

        obj_to_delete.status = 0
        obj_to_delete.save()

        active_Tasks = AdvertiserTaskList.objects.filter(status=1)
        ac_con = list(active_Tasks.values())

        contacts = {
            'active': ac_con,
        }

        return JsonResponse(contacts)

def create_contact (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)

        if data['id'] == 0:
            contact = CompanyContact(
                account_id=data['account'],
                first_name=data['firstname'],
                last_name=data['lastname'],
                full_name=data['firstname'] + " " + data['lastname'],
                email=data['email'],
                department_id=data['department'],
                phone_number=data['phone'],
                default=data['default'],
                active=1
            )
            contact.save()

        if data['id'] != 0:
            print("==============update=================")
            contact = CompanyContact.objects.get(id=data['id'])

            contact.account_id = data['account']
            contact.first_name = data['firstname']
            contact.last_name = data['lastname']
            contact.email = data['email']
            contact.department_id = data['department']
            contact.phone_number = data['phone']
            contact.full_name = data['firstname'] + " " + data['lastname']
            contact.default = data['default']

            contact.save()

        active_contacts = CompanyContact.objects.filter(active=1)
        ac_con = list(active_contacts.values())

        inactive_contacts = CompanyContact.objects.filter(active=0)
        inac_con = list(inactive_contacts.values())

        contacts = {
            'active': ac_con,
            'inactive': inac_con,
        }

        return JsonResponse(contacts)
def get_id_contact (request) :
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        search_contacts = Account.objects.filter(id=data['id'])
        contacts = list(search_contacts.values())
        return JsonResponse(contacts)

def getTaskList (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        if data['status'] == 'active':
            active_Tasks = AdvertiserTaskList.objects.filter(status=1)
            ac_con = list(active_Tasks.values())

            contacts = {
                'active': ac_con,
            }

            return JsonResponse(contacts)
        if data['status'] == 'complete':
            active_Tasks = AdvertiserTaskList.objects.filter(complete=1)
            ac_con = list(active_Tasks.values())

            contacts = {
                'active': ac_con,
            }

            return JsonResponse(contacts)

def search_filter_contacts (request):
    if request is None or not request.user.is_authenticated:
        return redirect(login_redirect + "dashboard.html")

    if not request.user.has_perm('BI.advertising_access'):
        return render(request, "dashboard.html",
                      {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        data = json.loads(body)
        if data['param'] == 'all':
            active_contacts = CompanyContact.objects.filter(active=1)
            ac_con = list(active_contacts.values())

            inactive_contacts = CompanyContact.objects.filter(active=0)
            inac_con = list(inactive_contacts.values())

            contacts = {
                'active': ac_con,
                'inactive': inac_con,
            }

            return JsonResponse(contacts)
        if data['param'] == 'search':
            active_contacts = CompanyContact.objects.filter(full_name__contains=data['search_val'], active=1)
            ac_con = list(active_contacts.values())

            inactive_contacts = CompanyContact.objects.filter(full_name__contains=data['search_val'],active=0)
            inac_con = list(inactive_contacts.values())

            contacts = {
                'active': ac_con,
                'inactive': inac_con,
            }
            return JsonResponse(contacts)
        if data['param'] == 'filter':

            if data['status'] == 2:
                if data['dept'] == 0:
                    active_contacts = CompanyContact.objects.filter(active=1)
                    ac_con = list(active_contacts.values())

                    inactive_contacts = CompanyContact.objects.filter(active=0)
                    inac_con = list(inactive_contacts.values())

                elif data['dept'] != 0:
                    active_contacts = CompanyContact.objects.filter(department_id=data['dept'],active=1)
                    ac_con = list(active_contacts.values())

                    inactive_contacts = CompanyContact.objects.filter(department_id=data['dept'], active=0)
                    inac_con = list(inactive_contacts.values())
                contacts = {
                    'active': ac_con,
                    'inactive': inac_con,
                }

                return JsonResponse(contacts)
            elif data['status'] != 2:
                if data['status'] == 1:
                    if data['dept'] == 0:
                        active_contacts = CompanyContact.objects.filter(active=1)
                        ac_con = list(active_contacts.values())
                    elif data['dept'] != 0:
                        active_contacts = CompanyContact.objects.filter(department_id=data['dept'],active=1)
                        ac_con = list(active_contacts.values())
                    contacts = {
                        'active': ac_con,
                        'inactive': ''
                    }
                    return JsonResponse(contacts)
                elif data['status'] == 0:
                    if data['dept'] == 0:
                        inactive_contacts = CompanyContact.objects.filter(active=0)
                        inac_con = list(inactive_contacts.values())
                    elif data['dept'] != 0:
                        inactive_contacts = CompanyContact.objects.filter(department_id=data['dept'], active=0)
                        inac_con = list(inactive_contacts.values())
                    contacts = {
                        'active': '',
                        'inactive': inac_con
                    }
                    return JsonResponse(contacts)