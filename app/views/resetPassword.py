from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from app.models import ProfileModel
# from furnitureapp.helpers import send_forget_password_mail
import uuid

def changepassword(request, token):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"/change-password/{token}/")

        try:
            profile_obj = ProfileModel.objects.get(forget_password_token=token)
            user = profile_obj.user
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully. Please login.")
            return redirect("/login")
        except ProfileModel.DoesNotExist:
            messages.error(request, "Invalid token.")
            return redirect("/login")

    return render(request, "change-password.html", {"token": token})

def forgetpassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No user found with this email.")
            return redirect("/forget-password/")

        token = str(uuid.uuid4())
        profile_obj, created = ProfileModel.objects.get_or_create(user=user)
        profile_obj.forget_password_token = token
        profile_obj.save()
        # send_forget_password_mail(user.email, token)

        messages.success(request, "An email is sent")
        return redirect("/forget-password/")

    return render(request, "forget-password.html")
