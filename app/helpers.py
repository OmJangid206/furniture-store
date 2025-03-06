# helpers.py
from django.core.mail import send_mail
from django.conf import settings
import requests
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from six import text_type
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login
from app.utils import TokenGenerator

generate_token = TokenGenerator()

def send_forget_password_mail(email, token):
    subject = "Your forget password link"
    message = f"Hi, click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    # Disable SSL certificate verification (for local testing only)
    response = requests.post("http://127.0.0.1:8000/forget-password/", verify=False)


def register(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        # if User.objects.filter(username=username):
        #   messages.error(request,'Username already exists')
        #   return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect("home")
        # if len(username)>10:
        #   messages.error(request,'Please create an username with less than 10 characters')
        #   return redirect('home')
        if pass1 != pass2:
            messages.error(
                request, "confirmed password doesnt match with typed password"
            )
            return redirect("home")
        else:
            myuser = User.objects.create_user(email, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()
            messages.success(
                request,
                "Your account has been successfully created,please check your email for activating your account",
            )

        # welcome email
        subject = "Welcome to E-Panchayat login"
        message = (
            "Hello!"
            + myuser.first_name
            + "Welcome to E-Panchayat\n Thank you for visiting our website\n We also have sent you a confirmation email, Please confirm your email address to activate your account\n Thank You"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        # Confirmation Email to email address

        current_site = get_current_site(request)
        email_subject = "Confirm your email address for E-Panchayat"
        message2 = render_to_string(
            "emailconfirmation.html",
            {
                "name": myuser.first_name,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token": generate_token.make_token(myuser),
            },
        )
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()
        return render(request, "register.html")
    return render(request, "register.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "registered and logged in successfully")
        return render(request, "upage.html")
    else:
        return render(request, "activationfailed.html")
