"""
models/feedback_model.py

This module defines the `FeedbackModel` class, which represents user feedback 
submitted through the application.

It provides functionalities to:
- Store user feedback, including name, email, and feedback description.
- Retrieve feedback details.

Classes:
    - FeedbackModel: Represents a user feedback entry.
"""

from django.db import models


class FeedbackModel(models.Model):
    """
    Represents user feedback in the application.

    Attributes:
        name (str): The name of the user submitting the feedback (max length: 50 characters).
        email (str): The email address of the user.
        feedback_description (str): The detailed feedback provided by the user.
    """
    name = models.CharField(max_length=50)
    email = models.EmailField()
    feedback_description = models.TextField()

    class Meta:
        verbose_name_plural = "Feedbacks"  

    def __str__(self):
        """
        Returns a string representation of the feedback entry.

        Returns:
            str: The name of the user who submitted the feedback.
        """
        return self.name
    