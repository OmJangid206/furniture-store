"""
This module contains the class-based view for updating the user's profile.

The `UpdateProfileView` class handles displaying the profile form and processing 
the form submission to update the user's profile.
Only authenticated users can access this view.

Classes:
    UpdateProfileView (View): A view for updating the user's profile with 
    the option to upload a new profile image.
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.views import View
from app.forms.user_form import ProfileForm
from app.models.profile_model import ProfileModel
from app.utils.common_utils import get_cart_count

@method_decorator(login_required(login_url="login"), name="dispatch")
class UpdateProfileView(View):
    """
    A class-based view for updating the user's profile.

    This view handles both displaying the profile form and saving the updated profile data.
    Only authenticated users can access this view.

    Attributes:
        request: The HTTP request object.
    
    Methods:
        get: Displays the profile form with existing user data.
        post: Handles form submission to update the profile.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Displays the profile form with existing data for the user.

        Args:
            request: The HTTP request object.

        Returns:
            Rendered profile update page with the profile form.
        """
        # Retrieve or create a profile for the user
        profile, _ = ProfileModel.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile)
        cart_count = get_cart_count(request.user)
        context = {"form": form, "cart_count": cart_count}
        return render(request, "update-profile.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles form submission to update the profile.

        Args:
            request: The HTTP request object.

        Returns:
            Redirects to the profile page upon successful form submission.
            If the form is invalid, reloads the update profile page with errors.
        """
        profile, _ = ProfileModel.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        print(f"form: {form}")
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile is updated.")
            return redirect("profile")
        else:
            messages.error(request, "Failed to update profile. Please check the form.")
            return render(request, "update-profile.html", {"form": form, "cart_count": get_cart_count(request.user)})
