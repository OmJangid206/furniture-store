from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from app.middlewares.auth_middlewares import unauthentcated_user
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from config import settings
from app.models import ProfileModel
from app.forms import ProfileForm
from app.utils import get_cart_count, TokenGenerator


generate_token = TokenGenerator()


# Login
@method_decorator(unauthentcated_user, name="dispatch")
class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get("return_url")
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session.pop("return_to", None)
            if Login.return_url:
                return HttpResponseRedirect(Login.return_url)
            else:
                return redirect("/")
        else:
            messages.error(request, "Wrong password or username")
            return redirect("login")


# Profile view
@login_required(login_url="login")
def profile(request):
    cart_count = get_cart_count(request.user)
    return render(request, "profile.html", {"cart_count": cart_count})


# SignUp Page
def signup(request):
    # form = CreateUserFrom()
    # if request.method == "POST":
    #     form = CreateUserFrom(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Account is Created")
    #         return redirect("login")
    #     else:
    #         context = {"form": form}
    #         messages.error(request, "Invalid credentials")
    #         return render(request, "signup.html", context)
    # context = {"form": form}

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
            return render(request, "signup.html")

        # if len(username)>10:
        #   messages.error(request,'Please create an username with less than 10 characters')
        #   return redirect('home')
        if pass1 != pass2:
            messages.error(
                request, "confirmed password doesnt match with typed password"
            )
            return render(request, "signup.html")
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
        subject = "Welcome to Shanti Furniture E-shop login"
        message = (
            "Hello!"
            + myuser.first_name
            + "Welcome to Shanti Furniture E-shop\n Thank you for visiting our website\n We also have sent you a confirmation email, Please confirm your email address to activate your account\n Thank You"
        )
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirmation Email to email address
        current_site = get_current_site(request)
        email_subject = "Confirm your email address for Shanti Furniture"
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
        return render(request, "signup.html")
    return render(request, "signup.html")
    # return render(request, "signup.html", context)


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
        cart_count = get_cart_count(request.user)  # Get cart count here
        return render(request, "thankyouregister.html", {"cart_count": cart_count})
    else:
        return render(request, "activationfailed.html")


# UpdateProfile
@login_required(login_url="login")
def updateprofile(request):
    # Retrieve the profile or create a new one
    profile, created = ProfileModel.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile is updated.")
            return redirect("profile")
        else:
            print(form.errors)
            messages.error(request, "Failed to update profile. Please check the form.")
    else:
        form = ProfileForm(instance=profile)

    cart_count = get_cart_count(request.user)
    context = {"form": form, "cart_count": cart_count}
    return render(request, "updateprofile.html", context)


# logout
@login_required(login_url="login")
def logout_user(request):
    return_url = request.session.pop("return_to", "/")
    logout(request)
    messages.info(request, "You are logged out successfully ")
    return redirect(return_url)
