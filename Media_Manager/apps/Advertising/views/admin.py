
from ..models.orders import *
from django.shortcuts import render, redirect
from ..models.companies import *
from ..models.advertising import *

def admin(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/admin.html')

def adminGeneral(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/admin-general.html')

def adminAds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/ads/ads.html')

def adminFinancial(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/financial/admin-financial.html')

def adminFinancialFiscal(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/financial/fiscal-year.html')

def adminPricing(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/pricing/admin-pricing.html')

def adminPricingEditRate(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/pricing/edit-rate.html')

def adminNewPublication(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	adTypes = AdType.objects.all().order_by('name')
	gl_codes = GLCode.objects.all().order_by('id')
	adjustments = Adjustment.objects.all().order_by('id')	

	context = {
        "access": "allow",
        "message": "",
        "adTypes": adTypes,
        "gl_codes": gl_codes,
        "adjustments": adjustments
    }
	return render(request, 'admin/pubs/new-publication.html', context)

def adminNewMagazine(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/products/new-magazine.html')

def adminNewNewspaper(request):
  return render(request, 'admin/products/new-newspaper.html')

def adminNewDigital(request):
  return render(request, 'admin/products/new-digital.html')
