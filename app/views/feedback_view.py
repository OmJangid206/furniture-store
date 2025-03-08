"""
views/feedback_view.py

This module defines the `FeedbackView` class, which handles feedback-related requests 
in the application.

It provides functionalities to:
- Render the feedback form page.
- Process and store user feedback submissions.

Classes:
    - FeedbackView: Handles GET and POST requests for the feedback page.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from app.models.feedback_model import FeedbackModel
from django.views import View
from app.utils.common_utils import get_cart_count


class FeedbackView(View):
    """
    Handles feedback form interactions.

    This view allows users to submit feedback, which is stored in the database.
    The feedback page also displays the user's cart count.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Handles GET requests for the feedback page.

        Retrieves the user's cart count and renders the feedback form.

        Args:
            request (HttpRequest): The HTTP request instance.

        Returns:
            HttpResponse: The rendered 'feedback.html' page with cart count.
        """
        context = {"cart_count": get_cart_count(request.user)}
        return render(request, "feedback.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Handles POST requests for feedback submission.

        Extracts user input from the request, saves the feedback, 
        and renders the page with a success message.

        Args:
            request (HttpRequest): The HTTP request instance containing feedback data.

        Returns:
            HttpResponse: The rendered 'feedback.html' page with cart count and success message.
        """
 
        feedback_model = FeedbackModel(
            name=request.POST.get("name"), 
            email=request.POST.get("email"), 
            feedback_description=request.POST.get("desc")
        )
        feedback_model.save()

        context = {
            "cart_count": get_cart_count(request.user), 
            "message": "Your feedback has been saved."
        }
        return render(request, "feedback.html", context)
