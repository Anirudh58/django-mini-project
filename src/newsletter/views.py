from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail

from .forms import SignUpForm, ContactForm
from .models import SignUp 

# Create your views here

def  home(request):
	title = "Send us your complaint! "


	# if request.method == "POST":
	# 	print request.POST
		
	form = SignUpForm(request.POST or None)

	context = {
		"title": title,
		"form": form
	}


	if form.is_valid():
		instance = form.save(commit = False)

		if not instance.full_name:
			instance.full_name = "Anonymous"

		instance.save()

		print instance.full_name
		print instance.email
		print instance.complaint
		print instance.timestamp

		context = {
			"title" : "Your complaint has been registered!"
		}

	if request.user.is_authenticated() and request.user.is_staff :
		#print SignUp.objects.all()
		
		for item in SignUp.objects.all():
			print item

		queryset = SignUp.objects.all()
		context = {

			"queryset" : queryset,
		}

	
	return render(request, "home.html", context)


def contact(request):
	form = ContactForm(request.POST or None)
	title = "Contact Form"
	context = {

		"form" : form,
		"title" : title,
	}

	if form.is_valid():

		email = form.cleaned_data["email"]
		full_name = form.cleaned_data["full_name"]
		message = form.cleaned_data["message"]

		subject = "Site Contact Form"
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, "vvedavalli@yahoo.com"]
		contact_message = " %s %s via %s hello maam" % (full_name, message, email)

		send_mail(subject, contact_message, from_email, to_email, fail_silently = False)



	return render(request, "forms.html", context)