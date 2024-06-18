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

# def adminUpload(request):
# 	# Check if user is logged in, if not, redirect  to login screen
# 	if request is None or not request.user.is_authenticated:
# 		return redirect(login_redirect + '/')
# 	success = False
# 	file_name = ''
# 	if request.method == 'POST' and 'file' in request.FILES:
# 		uploaded_file = request.FILES['file']
# 		current_time = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # Get timestamp with milliseconds
# 		file_name = f"{current_time}_{uploaded_file.name}"
# 		file_path = os.path.join('uploads', file_name)
		
# 		with open(file_path, 'wb+') as destination:
# 			for chunk in uploaded_file.chunks():
# 				destination.write(chunk)
# 		success = True
# 	return JsonResponse({'success': success, "url": f"/uploads/{file_name}"}, status=200)

def adminGeneral(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	all_states = AllStates.objects.all()
	magazines = MagazineProduct.objects.all()
	newspapers = NewspaperProduct.objects.all()
	digitals = DigitalProduct.objects.all()
	regions = Region.objects.all()
	publications = AdminPublication.objects.all()
	context = {
		'all_states': all_states,
		'magazines': magazines,
		'newspapers': newspapers,
		'regions': regions,
		'publications': publications,
		'total_newspapers': len(newspapers),
		'total_magazines': len(magazines),
		'total_digitals': len(digitals),
		'digitals': digitals,
	}
	return render(request, 'admin/admin-general.html', context)

def adminAds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	pub_adtypes = PubAdType.objects.all()
	adtypes = AdminAdType.objects.all()
	rates = Rate.objects.all()
	publications = AdminPublication.objects.all()
	marketcodes = AdminMarketCode.objects.all()
	context = {
		'pub_adtypes': pub_adtypes,
		'adtypes': adtypes,
		'rates': rates,
		'marketcodes': marketcodes,
		'publications': publications
	}
	return render(request, 'admin/ads/ads.html', context)
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
			publication = AdminPublication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=adtype, adminpublication=publication)
			new_pub_adtype.save()
	except Exception as e:
		success = False

	return JsonResponse({'success': success, "errors": []}, status=200)
def adminAdsAdTypeDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	adtype = AdminAdType.objects.get(pk=data['id'])
	pub_adtypes = PubAdType.objects.filter(adminadtype=adtype.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.publication.id, 'name': pa.publication.name} for pa in pub_adtypes]
	pub_ids = []
	for pub_adtype in pub_adtypes:
		pub_ids.append(pub_adtype.publication.id)

	pub_adtypes = AdminPublication.objects.exclude(id__in=pub_ids)
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
			publication = AdminPublication.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype=new_adtype, adminpublication=publication)
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
	pub_adjustments = PubAdjustment.objects.filter(adminadjustment=adjustment.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.publication.id, 'name': pa.publication.name} for pa in pub_adjustments]
	pub_ids = []
	for pub_adjustment in pub_adjustments:
		pub_ids.append(pub_adjustment.publication.id)

	pub_adjustments = AdminPublication.objects.exclude(id__in=pub_ids)
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
	publications = AdminPublication.objects.all()
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
		publication = AdminPublication.objects.get(pk=id)
		new_pub_adjustment = PubAdjustment(adminadjustment=adjustment, adminpublication=publication)
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
		publication = AdminPublication.objects.get(pk=id)
		new_pub_adjustment = PubAdjustment(adminadjustment=new_adjustment, adminpublication=publication)
		new_pub_adjustment.save()
	return JsonResponse({"errors": []}, status=200)

def adminPricingSaveRateGroup(request, groupId):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	print(data)
	rategroup = RateGroup.objects.get(pk=groupId)
	rategroup.name = data['name']
	rategroup.description = data['description']
	if data['status'] != -1:
		rategroup.status = data['status']
	if data['active'] != -1:
		rategroup.active = data['active']
	success = True
	try:
		rategroup.save()
		publications = PubRategroup.objects.filter(rategroup=rategroup)
		for publication in publications:
			publication.delete()
		pub_ids = json.loads(data['assigned_publications'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = publication)
			new_pub_rategroup.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)

def adminPricingSaveRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	rate = Rate.objects.get(pk = int(data['id']))
	rate.name=data['name']
	rate.pricing=data['pricing']
	rate.measurement_type=data['measurement_type']
	rate.tax_category=data['tax_category']
	rate.override_privileges=data['override_privileges']
	rate.assigned_groups=data['assigned_groups']
	rate.ad_type_id=data['ad_type']
	rate.start_date=data['start_date']
	rate.end_date=data['end_date']
	rate.insertion_min=data['insertion_min']
	rate.insertion_max=data['insertion_max']
	rate.line_for_ad_min=data['line_for_ad_min']
	rate.line_for_ad_max=data['line_for_ad_max']
	rate.insertion_count=data['insertion_count']
	rate.base_cost=data['base_cost']
	rate.base_count=data['base_count']
	rate.additional_cost=data['additional_cost']
	rate.additional_count=data['additional_count']
	rate.charge_for=data['charge_for']
	rate.default_gl_code_id=data['default_gl_code']
	success = True
	try:
		rate.save()
		# extra_groups = ExtraRateGroup.objects.filter(rate = rate)
		# for group in extra_groups:
		# 	group.delete()
		# extra_groups = json.loads(data['extra_groups'])
		# for id in extra_groups:
		# 	rategroup = RateGroup.objects.get(pk=id)
		# 	new_extra_group = ExtraRateGroup(rate=rate, rategroup=rategroup)
		# 	new_extra_group.save()
	except Exception as e:
		print(e)
		success = False
	return JsonResponse({"success": success}, status=200)

def adminPricingEditRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	print(data)
	rate = Rate.objects.get(pk = data['id'])
	extra_groups = ExtraRateGroup.objects.filter(rate = data['id']).select_related('rategroup')
	assigned_groups = [{'id': pa.rategroup.id, 'name': pa.rategroup.name} for pa in extra_groups]
	print(assigned_groups)
	response_data = {
			'id': rate.id,
			'rate': serializers.serialize('json', [rate]),
			'start_date': rate.start_date.isoformat(),
			'end_date': rate.end_date.isoformat(),
			'assigned_groups': assigned_groups,
	}
	return JsonResponse(response_data)

def adminPricingCreateRateGroup(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	rategroup = RateGroup(name = data['name'], description = data['description'], active = data['active'])
	success = True
	try:
		rategroup.save()
		pub_ids = json.loads(data['publication_id'])
		for id in pub_ids:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = publication)
			new_pub_rategroup.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)
def adminPricingEditRateGroup(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	rategroup = RateGroup.objects.get(pk=groupId)
	publications = AdminPublication.objects.all()
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
	pub_rategroups = PubRategroup.objects.filter(rategroup=rategroup.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.adminpublication.id, 'name': pa.adminpublication.name} for pa in pub_rategroups]
	pub_ids = []
	for pub_rategroup in pub_rategroups:
		pub_ids.append(pub_rategroup.adminpublication.id)

	pub_rategroups = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in pub_rategroups]
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
	return render(request, 'admin/pricing/edit-rategroup.html', context)

def adminPricingCreateRate(request, groupId):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_rate = Rate(name=data['name'], pricing=data['pricing'], measurement_type=data['measurement_type'], tax_category=data['tax_category'], override_privileges=data['override_privileges'], 
								 assigned_groups=data['assigned_groups'], ad_type_id=data['ad_type'], start_date=data['start_date'], end_date=data['end_date'],
								 insertion_min=data['insertion_min'], insertion_max=data['insertion_max'], line_for_ad_min=data['line_for_ad_min'], line_for_ad_max=data['line_for_ad_max'],
								 insertion_count=data['insertion_count'], base_cost=data['base_cost'], base_count=data['base_count'], additional_cost=data['additional_cost'], 
								 additional_count=data['additional_count'], charge_for=data['charge_for'], default_gl_code_id=data['default_gl_code'])
	success = True
	try:
		new_rate.save()
		extra_groups = json.loads(data['extra_groups'])
		for id in extra_groups:
			rategroup = RateGroup.objects.get(pk=id)
			new_extra_group = ExtraRateGroup(rate=new_rate, rategroup=rategroup)
			new_extra_group.save()
	except Exception as e:
		success = False
	return JsonResponse({"success": success}, status=200)
def adminClassifieds(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	publications = [
			{'name': 'Publication 1', 'value': 'publication-1'},
			{'name': 'Publication 2', 'value': 'publication-2'},
	]
	
	# Add the arrays to the context
	context = {
			'publications': publications,
	}
	return render(request, 'admin/classifieds/classifieds.html', context)
def adminSavePublication(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	pub = AdminPublication.objects.get(pk=id)
	pub.name = data['name']
	pub.address = data['address']
	pub.city = data['city']
	pub.state_id = data['state']
	pub.zip_code = data['zip_code']
	pub.product_name = data['product_name']
	pub.gl_override = data['gl_override']
	pub.gl_code_id = data['gl_code']
	pub.start_date = data['start_date']
	pub.end_date = data['end_date']
	pub.calendar_type = data['calendar_type']
	pub.product_type = data['product_type']
	pub.active = data['active']
	pub.status = data['status']
	success = True
	try:
		pub.save()
		rategroups = PubRategroup.objects.filter(adminpublication=pub)
		for rategroup in rategroups:
			rategroup.delete()
		rategroup_ids = json.loads(data['rategroup_id'])
		for id in rategroup_ids:
			rategroup = RateGroup.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = pub)
			new_pub_rategroup.save()
		adminadtypes = PubAdType.objects.filter(adminpublication=pub)
		for adminadtype in adminadtypes:
			adminadtype.delete()
		adtype_ids = json.loads(data['adtype_id'])
		for id in adtype_ids:
			adtype = AdminAdType.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype = adtype, adminpublication = pub)
			new_pub_adtype.save()
		adminadjustments = PubAdjustment.objects.filter(adminpublication=pub)
		for adminadjustment in adminadjustments:
			adminadjustment.delete()
		adjustment_ids = json.loads(data['adjustment_id'])
		for id in adjustment_ids:
			adjustment = AdminAdjustment.objects.get(pk=id)
			new_pub_adjustment = PubAdjustment(adminadjustment = adjustment, adminpublication = pub)
			new_pub_adjustment.save()
		sections = PubSection.objects.filter(adminpublication=pub)
		for section in sections:
			section.delete()
		section_ids = json.loads(data['section_id'])
		for id in section_ids:
			section = PublicationSection.objects.get(pk=id)
			new_pub_section = PubSection(section = section, adminpublication = pub)
			new_pub_section.save()
	except Exception as e:
		success = False
	return JsonResponse({'success': success}, status = 200)
def adminCreatePublication(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_publication = AdminPublication(name = data['name'], address = data['address'], city = data['city'], state_id = int(data['state']), zip_code=data['zip_code'],
																		location = '', parent_id = data['parent_id'], product_name = data['product_name'], gl_override = data['gl_override'],account = 'Times Leader',
																		gl_code_id = int(data['gl_code']), start_date = data['start_date'], end_date = data['end_date'], created_by = data['created_by'],
																		calendar_type = data['calendar_type'], product_type = data['product_type'])
	success = True
	try:
		new_publication.save()
		rategroup_ids = json.loads(data['rategroup_id'])
		for id in rategroup_ids:
			rategroup = RateGroup.objects.get(pk=id)
			new_pub_rategroup = PubRategroup(rategroup = rategroup, adminpublication = new_publication)
			new_pub_rategroup.save()
		adtype_ids = json.loads(data['adtype_id'])
		for id in adtype_ids:
			adtype = AdminAdType.objects.get(pk=id)
			new_pub_adtype = PubAdType(adminadtype = adtype, adminpublication = new_publication)
			new_pub_adtype.save()
		adjustment_ids = json.loads(data['adjustment_id'])
		for id in adjustment_ids:
			adjustment = AdminAdjustment.objects.get(pk=id)
			new_pub_adjustment = PubAdjustment(adminadjustment = adjustment, adminpublication = new_publication)
			new_pub_adjustment.save()
		section_ids = json.loads(data['section_id'])
		for id in section_ids:
			section = PublicationSection.objects.get(pk=id)
			new_pub_section = PubSection(section = section, adminpublication = new_publication)
			new_pub_section.save()
	except Exception as e:
		success = False
	return JsonResponse({'success': success}, status = 200)
def adminEditPublication(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	pub = AdminPublication.objects.get(pk=id)
	gl_codes = GLCode.objects.all()
	publications = AdminPublication.objects.all()
	all_states = AllStates.objects.all()
	pub_rategroups = PubRategroup.objects.filter(adminpublication=pub.id).select_related('rategroup')
	assigned_rategroups = [{'id': pa.rategroup.id, 'name': pa.rategroup.name} for pa in pub_rategroups]
	rategroup_ids = []
	for pub_rategroup in pub_rategroups:
		rategroup_ids.append(pub_rategroup.rategroup.id)

	unsigned = RateGroup.objects.exclude(id__in=rategroup_ids)
	unsigned_rategroups = [{'id': pa.id, 'name': pa.name} for pa in unsigned]

	pub_adminadtypes = PubAdType.objects.filter(adminpublication=pub.id).select_related('adminadtype')
	assigned_adminadtypes = [{'id': pa.adminadtype.id, 'name': pa.adminadtype.name} for pa in pub_adminadtypes]
	adminadtype_ids = []
	for pub_adminadtype in pub_adminadtypes:
		adminadtype_ids.append(pub_adminadtype.adminadtype.id)

	unsigned = AdminAdType.objects.exclude(id__in=adminadtype_ids)
	unsigned_adminadtypes = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	
	pub_adminadjustments = PubAdjustment.objects.filter(adminpublication=pub.id).select_related('adminadjustment')
	assigned_adminadjustments = [{'id': pa.adminadjustment.id, 'name': pa.adminadjustment.name} for pa in pub_adminadjustments]
	adminadjustment_ids = []
	for pub_adminadjustment in pub_adminadjustments:
		adminadjustment_ids.append(pub_adminadjustment.adminadjustment.id)

	unsigned = AdminAdjustment.objects.exclude(id__in=adminadjustment_ids)
	unsigned_adminadjustments = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	
	pub_sections = PubSection.objects.filter(adminpublication=pub.id).select_related('section')
	assigned_sections = [{'id': pa.section.id, 'name': pa.section.name} for pa in pub_sections]
	section_ids = []
	for pub_section in pub_sections:
		section_ids.append(pub_section.section.id)

	unsigned = PublicationSection.objects.exclude(id__in=section_ids)
	unsigned_sections = [{'id': pa.id, 'name': pa.name} for pa in unsigned]
	context = {
        "access": "allow",
        "message": "",
        "gl_codes": gl_codes,
				"publications": publications,
				"all_states": all_states,
				"assigned_rategroups": assigned_rategroups,
				"unsigned_rategroups": unsigned_rategroups,
				"assigned_adminadtypes": assigned_adminadtypes,
				"unsigned_adminadtypes": unsigned_adminadtypes,
				"assigned_adminadjustments": assigned_adminadjustments,
				"unsigned_adminadjustments": unsigned_adminadjustments,
				"assigned_sections": assigned_sections,	
				"unsigned_sections": unsigned_sections,
				"pub": pub,
				"start_date": pub.start_date.isoformat(),
				"end_date": pub.end_date.isoformat()
    }
	return render(request, 'admin/pubs/edit-publication.html', context)
def adminNewPublication(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	
	adTypes = AdminAdType.objects.all()
	gl_codes = GLCode.objects.all()
	adjustments = AdminAdjustment.objects.all()
	rategroups = RateGroup.objects.all()
	sections = PublicationSection.objects.all()
	publications = AdminPublication.objects.all()
	all_states = AllStates.objects.all()
	context = {
        "access": "allow",
        "message": "",
        "adtypes": adTypes,
        "gl_codes": gl_codes,
        "adjustments": adjustments,
				"rategroups": rategroups,
				"sections": sections,
				"publications": publications,
				"all_states": all_states
    }
	return render(request, 'admin/pubs/new-publication.html', context)

def adminNewMagazine(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request.method == 'GET':
		standardsizes = StandardSize.objects.filter(type = 1)
		return render(request, 'admin/products/new-magazine.html', {'standardsizes': standardsizes})
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
def adminEditMagazine(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = MagazineProduct.objects.get(pk=id)
	standardsizes = StandardSize.objects.filter(type = 1)
	return render(request, 'admin/products/edit-magazine.html', {'product': product, 'standardsizes': standardsizes})

def adminSaveMagazine(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = MagazineProduct.objects.get(pk=id)
	product.product_mag = data['product_mag']
	product.measurement_type = data['measurement_type']
	product.fold_orientation = data['fold_orientation']
	product.height = data['height']
	product.width = data['width']
	product.columns = data['columns']
	product.column_width = data['column_width']
	product.page_width = data['page_width']
	product.page_height = data['page_height']
	product.page_border = data['page_border']
	product.gutter_size = data['gutter_size']
	success = True
	try:
		product.save()
	except Exception as e:
		success = False
	return JsonResponse({'success': success}, status = 200)

def adminNewNewspaper(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request.method == 'GET':
		standardsizes = StandardSize.objects.filter(type = 2)
		return render(request, 'admin/products/new-newspaper.html', {'standardsizes': standardsizes})
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

def adminEditNewspaper(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = NewspaperProduct.objects.get(pk=id)
	standardsizes = StandardSize.objects.filter(type = 2)
	return render(request, 'admin/products/edit-newspaper.html', {'product': product, 'standardsizes': standardsizes})

def adminSaveNewspaper(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = NewspaperProduct.objects.get(pk=id)
	product.product_mag = data['product_mag']
	product.measurement_type = data['measurement_type']
	product.fold_orientation = data['fold_orientation']
	product.height = data['height']
	product.width = data['width']
	product.columns = data['columns']
	product.column_width = data['column_width']
	product.page_width = data['page_width']
	product.page_height = data['page_height']
	product.page_border = data['page_border']
	product.gutter_size = data['gutter_size']
	success = True
	try:
		product.save()
	except Exception as e:
		success = False
	return JsonResponse({'success': success}, status = 200)

def adminNewDigital(request):
	if request.method == 'GET':
		adtypes = AdminAdType.objects.all()
		standardsizes = StandardSize.objects.filter(type = 3)
		return render(request, 'admin/products/new-digital.html', {'adtypes': adtypes, 'standardsizes': standardsizes})
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

def adminEditDigital(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	product = DigitalProduct.objects.get(pk=id)
	adtypes = AdminAdType.objects.all()
	standardsizes = StandardSize.objects.filter(type = 3)
	return render(request, 'admin/products/edit-digital.html', {'product': product, 'standardsizes': standardsizes, 'adtypes': adtypes})

def adminSaveDigital(request, id):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	body = request.body.decode('utf-8')
	data = json.loads(body)
	product = DigitalProduct.objects.get(pk=id)
	product.product_mag = data['product_mag']
	product.format = data['format']
	product.adminadtype_id = data['adminadtype']
	product.height = data['height']
	product.width = data['width']
	success = True
	try:
		product.save()
	except Exception as e:
		success = False
	return JsonResponse({'success': success}, status = 200)

def adminCreateStandardSize(request):
	body = request.body.decode('utf-8')
	data = json.loads(body)
	standardsize = StandardSize(type = data['type'], description = data['description'], columns = data['columns'], height = data['height'])
	success = True
	try:
		standardsize.save()
	except Exception as e:
		success = False		
	return JsonResponse({'success': success, "errors": []}, status=200)
def adminCreateRegion(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_region = Region(name = data['name'], code = data['code'])
	success = True
	try:
		new_region.save()
		pub_regions = json.loads(data['publication_id'])
		for id in pub_regions:
			publication = AdminPublication.objects.get(pk=id)
			new_pub_region = PubRegion(region = new_region, adminpublication = publication)
			new_pub_region.save()
	except Exception as e:
		success = False
	return JsonResponse({"success":success, "errors": []}, status=200)
def adminEditRegion(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	region = Region.objects.get(pk=data['id'])
	region.name = data['name']
	region.code = data['code']
	region.active = data['active']
	region.status = data['status']
	region.save()
	pub_regions = PubRegion.objects.filter(region=region)
	for pub_region in pub_regions:
		pub_region.delete()

	pub_ids = json.loads(data['publication_id'])
	for id in pub_ids:
		publication = AdminPublication.objects.get(pk=id)
		new_pub_region = PubRegion(region=region, adminpublication=publication)
		new_pub_region.save()

	return JsonResponse({"errors": []}, status=200)
def adminRegionDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	region = Region.objects.get(pk=data['id'])
	pub_regions = PubRegion.objects.filter(region=region.id).select_related('adminpublication')
	assigned_publications = [{'id': pa.publication.id, 'name': pa.publication.name} for pa in pub_regions]
	pub_ids = []
	for pub_region in pub_regions:
		pub_ids.append(pub_region.publication.id)

	unsigned = AdminPublication.objects.exclude(id__in=pub_ids)
	unsigned_publications = [{'id': pa.id, 'name': pa.name} for pa in unsigned] 

	response_data = {
			'id': region.id,
			'region': serializers.serialize('json', [region]),
			'assigned_publications': assigned_publications,
			'unsigned_publications': unsigned_publications,
	}
	return JsonResponse(response_data, safe=False)
def adminCreateMarketCode(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + '/')
	data = json.loads(request.body.decode('utf-8'))
	new_adminmarketcode = AdminMarketCode(name = data['name'], code = data['code'])
	success = True
	try:
		new_adminmarketcode.save()
	except Exception as e:
		success = False
	return JsonResponse({"success":success, "errors": []}, status=200)
def adminEditMarketCode(request):
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "advertising")

	if not request.user.has_perm('BI.advertising_access'):
		return render(request, "advertising.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	data = json.loads(request.body.decode('utf-8'))
	marketcode = AdminMarketCode.objects.get(pk=data['id'])
	marketcode.name = data['name']
	marketcode.code = data['code']
	marketcode.active = data['active']
	marketcode.status = data['status']
	success = True
	try:
		marketcode.save()
	except Exception as e:
		success = False
	return JsonResponse({"success":success, "errors": []}, status=200)
def adminMarketCodeDetail(request):

	data = json.loads(request.body.decode('utf-8'))
	marketcode = AdminMarketCode.objects.get(pk=data['id'])

	response_data = {
			'id': marketcode.id,
			'marketcode': serializers.serialize('json', [marketcode]),
	}
	return JsonResponse(response_data, safe=False)