from django.db import models


class ContactModel(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name


class FeedbackModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    feedback_description = models.TextField()

    def __str__(self):
        return self.name


class ServiceModel(models.Model):
    service_name = models.CharField(max_length=50)

    @staticmethod
    def get_all_sevices():
        return ServiceModel.objects.all()

    def __str__(self):
        return self.service_name
