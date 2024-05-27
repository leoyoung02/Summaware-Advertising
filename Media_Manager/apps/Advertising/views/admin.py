from django.shortcuts import render, redirect
from ..models.advertising import *
from ..models.orders import *
from ..models.rates import *
from ..models.publications import *
from ..models.companies import *
from .... import views
from django.core import serializers
import json
import os
from datetime import datetime

def admin(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	return render(request, 'admin/admin.html')

def adminUpload(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	success = False
	if request.method == 'POST' and 'file' in request.FILES:
		uploaded_file = request.FILES['file']
		current_time = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # Get timestamp with milliseconds
		file_name = f"{current_time}_{uploaded_file.name}"
		file_path = os.path.join('uploads', file_name)
		
		with open(file_path, 'wb+') as destination:
			for chunk in uploaded_file.chunks():
				destination.write(chunk)
		success = True
	return JsonResponse({'success': success, "url": f"/uploads/{file_name}"}, status=200)

def adminGeneral(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	all_states = AllStates.objects.all()
	return render(request, 'admin/admin-general.html', {'all_states': all_states})

def adminAds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	pub_adtypes = PubAdType.objects.all()
	adtypes = AdminAdType.objects.all()
	rates = Rate.objects.all()
	publications = Publication.objects.all()
	return render(request, 'admin/ads/ads.html',{'pub_adtypes': pub_adtypes, 'adtypes': adtypes, 'rates': rates, 'publications': publications})
def adminAdsEditAdType(request):

	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
	
	data = json.loads(request.body.decode('utf-8'))
	adtype = AdminAdType.objects.get(pk=data['id'])
	adtype.name = data['name']
	adtype.code = data['code']
	adtype.default_rate_id = data['default_rate']
	adtype.active = data['active']
	adtype.status = data['status']
	success = True
	try:
		adtype.save()
		pub_adtypes = PubAdType.objects.filter(adminadtype=adtype)
		for pub_adtype in pub_adtypes:
			pub_adtype.delete()

		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = Publication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=adtype, publication=publication)
			new_pub_adtype.save()
	except Exception as e:
		success = False

	return JsonResponse({'success': success, "errors": []}, status=200)
def adminAdsAdTypeDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	adtype = AdminAdType.objects.get(pk=data['id'])
	pub_adtypes = PubAdType.objects.filter(adminadtype=adtype.id).select_related('publication')
	assigned_publications = [{'id': pa.publication.id, 'name': pa.publication.name} for pa in pub_adtypes]
	pub_ids = []
	for pub_adtype in pub_adtypes:
		pub_ids.append(pub_adtype.publication.id)

	pub_adtypes = Publication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_adtypes] 

	response_data = {
			'id': adtype.id,
			'adtype': serializers.serialize('json', [adtype]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)

def adminAdsCreateAdType(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})
	data = json.loads(request.body.decode('utf-8'))
	new_adtype = AdminAdType(code=data['code'], name=data['name'], default_rate_id=data['default_rate'])
	success = True
	try:
		new_adtype.save()
		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = Publication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=new_adtype, publication=publication)
			new_pub_adtype.save()
	except Exception as e:
		success = False
	
	return JsonResponse({'success': success, "errors": []}, status=200)
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
def adminAdjustmentDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	adjustment = AdminAdjustment.objects.get(pk=data['id'])
	pub_adjustments = PubAdjustment.objects.filter(adminadjustment=adjustment.id).select_related('publication')
	assigned_publications = [{'id': pa.publication.id, 'name': pa.publication.name} for pa in pub_adjustments]
	pub_ids = []
	for pub_adjustment in pub_adjustments:
		pub_ids.append(pub_adjustment.publication.id)

	pub_adjustments = Publication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_adjustments] 

	response_data = {
			'id': adjustment.id,
			'adjustment': serializers.serialize('json', [adjustment]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)

def adminPricing(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	rategroups = RateGroup.objects.all()
	adjustments = AdminAdjustment.objects.all()
	publications = Publication.objects.all()
	sections = PublicationSection.objects.all()
	glcodes = GLCode.objects.all()

	content = {'rategroups': rategroups, 'adjustments': adjustments, 'publications': publications, 'sections': sections, 'glcodes': glcodes}
	return render(request, 'admin/pricing/admin-pricing.html', content)

def adminEditAdjustment(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	adjustment = AdminAdjustment.objects.get(pk=data['id'])
	adjustment.name = data['name']
	adjustment.code = data['code']
	adjustment.apply_level = data['apply_level']
	adjustment.gl_code_id = data['gl_code']
	adjustment.type = data['type']
	adjustment.value_type = data['value_type']
	adjustment.value = data['value']
	adjustment.section_id = data['section']
	adjustment.prompt_for_value = data['prompt_for_value']
	adjustment.active = data['active']
	adjustment.status = data['status']
	adjustment.save()
	pub_adjustments = PubAdjustment.objects.filter(adminadjustment=adjustment)
	for pub_adjustment in pub_adjustments:
		pub_adjustment.delete()

	pub_ids = json.loads(data['publication_id'])
	for id in pub_ids:
		publication = Publication.objects.get(pk=id)
		new_pub_adjustment = PubAdjustment(adminadjustment=adjustment, publication=publication)
		new_pub_adjustment.save()

	return JsonResponse({"errors": []}, status=200)

def adminCreateAdjustment(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	new_adjustment = AdminAdjustment(name=data['name'], code=data['code'], gl_code_id=data['gl_code'], apply_level=data['apply_level'],
																	type=data['type'], value_type=data['value_type'], value=data['value'], section_id=data['section'],
																	prompt_for_value=data['prompt_for_value'])
	new_adjustment.save()
	pub_ids = json.loads(data['publication_id'])
	for id in pub_ids:
		publication = Publication.objects.get(pk=id)
		new_pub_adjustment = PubAdjustment(adminadjustment=new_adjustment, publication=publication)
		new_pub_adjustment.save()
	return JsonResponse({"errors": []}, status=200)

def adminPricingSaveRate(request, groupId):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	rategroup = RateGroup.objects.get(pk=groupId)
	rategroup.name = data['name']
	rategroup.description = data['description']
	rategroup.assigned_publications = data['assigned_publications']
	if data['status'] != -1:
		rategroup.status = data['status']
	if data['active'] != -1:
		rategroup.active = data['active']
	rategroup.save()
	return JsonResponse({"errors": []}, status=200)

def adminPricingEditRateGroup(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	rategroup = RateGroup.objects.get(pk=groupId)
	publications = Publication.objects.all()
	rate_id = ExtraRateGroup.objects.filter(rategroup=groupId)
	rate_ids = []
	for rate in rate_id:
		rate_ids.append(rate.rate.id)
	rates = Rate.objects.filter(id__in=rate_ids)
	assigned_publications = []
	unsigned_publications = publications
	adtypes = AdType.objects.all()
	glcodes = GLCode.objects.all()
	extra_groups = RateGroup.objects.exclude(id=groupId)
	if rategroup.assigned_publications:
		pub_ids = json.loads(rategroup.assigned_publications)
		assigned_publications = Publication.objects.filter(id__in=pub_ids)
		unsigned_publications = Publication.objects.exclude(id__in=pub_ids)
	context = {
		'rategroup': rategroup, 
		'assigned_publications': assigned_publications, 
		'publications': publications, 
		'unsigned_publications': unsigned_publications,
		'adtypes': adtypes,
		'glcodes': glcodes,
		'extra_groups': extra_groups,
		'rates': rates,
	}
	return render(request, 'admin/pricing/edit-rate.html', context)

def adminPricingCreateRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_rate = Rate(name=data['name'], pricing=data['pricing'], measurement_type=data['measurement_type'], tax_category=data['tax_category'], override_privileges=data['override_privileges'], 
								 assigned_groups=data['assigned_groups'], ad_type_id=data['ad_type'], start_date=data['start_date'], end_date=data['end_date'],
								 insertion_min=data['insertion_min'], insertion_max=data['insertion_max'], line_for_ad_min=data['line_for_ad_min'], line_for_ad_max=data['line_for_ad_max'],
								 insertions_count=data['insertions_count'], base_cost=data['base_cost'], lines_count=data['lines_count'], additional_cost=data['additional_cost'], 
								 additional_lines_count=data['additional_lines_count'], charge_for=data['charge_for'], default_gl_code_id=data['default_gl_code'])
	new_rate.save()
	extra_groups = json.loads(data['extra_groups'])
	for id in extra_groups:
		rategroup = RateGroup.objects.get(pk=id)
		new_extra_group = ExtraRateGroup(rate=new_rate, rategroup=rategroup)
		new_extra_group.save()
	return JsonResponse({"errors": []}, status=200)

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
	if request.method == 'GET':
		return render(request, 'admin/products/new-magazine.html')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = MagazineProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = MagazineProduct(
		id=new_id,
		product_mag =  data['product_mag'],
		measurement_type = data['measurement_type'],
		fold_orientation = data['fold_orientation'],
		height = data['height'],
		width = data['width'],
		columns = data['columns'],
		column_width = data['column_width'],
		page_width = data['page_width'],
		page_height = data['page_height'],
		page_border = data['page_border'],
		gutter_size = data['gutter_size']
	)
	task.save()
	return JsonResponse(data)

def adminNewNewspaper(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request.method == 'GET':
		return render(request, 'admin/products/new-newspaper.html')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = NewspaperProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = NewspaperProduct(
		id=new_id,
		product_mag =  data['product_mag'],
		measurement_type = data['measurement_type'],
		fold_orientation = data['fold_orientation'],
		height = data['height'],
		width = data['width'],
		columns = data['columns'],
		column_width = data['column_width'],
		page_width = data['page_width'],
		page_height = data['page_height'],
		page_border = data['page_border'],
		gutter_size = data['gutter_size']
	)
	task.save()
	return JsonResponse(data)

def adminNewDigital(request):
	if request.method == 'GET':
		adtypes = AdminAdType.objects.all()
		return render(request, 'admin/products/new-digital.html', {'adtypes': adtypes})
	body = request.body.decode('utf-8')
	data = json.loads(body)
	max_id = DigitalProduct.objects.all().order_by("-id").first()
	if max_id:
		max_id = max_id.id
	else:
		max_id = 0
	new_id = max_id + 1 if max_id is not None else 1
	task = DigitalProduct(
		id=new_id,
		product_mag =  data['product_mag'],
		format = data['format'],
		adminadtype_id = data['adminadtype'],
		height = data['height'],
		width = data['width'],
	)
	task.save()
	return JsonResponse(data)
