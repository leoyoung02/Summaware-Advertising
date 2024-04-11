from django.shortcuts import render, redirect
from django.http import HttpResponse
from ... import views

url = "192.241.131.173:8000"
login_redirect = "/login/?next="

def editorial_view(request):
	# Check if user is logged in, if not, redirect  to login screen
	if request is None or not request.user.is_authenticated:
		return redirect(login_redirect + "editorial")

	if not request.user.has_perm('BI.editorial_access'):
<<<<<<< HEAD
		return render(request, "coming_soon.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "menu": views.get_sidebar(request)}
	return render(request, "coming_soon.html", context)
=======
		return render(request, "editorial.html", {"access": "deny", "message": "Access denied!", "menu": views.get_sidebar(request)})

	context = {"access": "allow", "message":"", "groups": ', '.join(views.get_groups(request)), "menu": views.get_sidebar(request)}
	return render(request, "editorial.html", context)
>>>>>>> 7a937277d63f6c5c5670567696935b34e97526a0
