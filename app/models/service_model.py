"""
models/service_model.py

This module defines the `ServiceModel` class, which represents services 
available in the application.

It provides functionalities to:
- Store service-related data.
- Retrieve all available services from the database.

Classes:
    - ServiceModel: Represents a service and provides methods to fetch service data.
"""

from django.db import models


class ServiceModel(models.Model):
    """
    Represents a service in the application.

    Attributes:
        service_name (str): The name of the service (max length: 50 characters).
    """
    service_name = models.CharField(max_length=50)

    class Meta:
        db_table = "service"
        verbose_name_plural = "Services" 

    @staticmethod
    def get_all_sevices():
        """
        Retrieves all available services from the database.

        Returns:
            QuerySet: A queryset containing all `ServiceModel` instances.
        """
        return ServiceModel.objects.all()

    def __str__(self):
        """
        Returns a string representation of the service.

        Returns:
            str: The name of the service.
        """
        return self.service_name
