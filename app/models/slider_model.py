from django.db import models


class SliderModel(models.Model):
    s_name = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to="slider/")

    @staticmethod
    def get_all_slider():
        return SliderModel.objects.all()

    def __str__(self):
        return self.s_name
