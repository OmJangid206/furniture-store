"""
model/slider_model.py

This module contains the `SliderModel` class used for storing slider data in the database. 

The `SliderModel` class allows for storing slider images with associated names. 
These sliders can be used in a variety of places in the application, such as on the homepage 
or in galleries, with each slider having an image and a name.

Classes:
    SliderModel (models.Model): A model for storing slider information, including the name of the slider and the image associated with it.
"""
from django.db import models
from cloudinary.models import CloudinaryField


class SliderModel(models.Model):
    """
    Model for storing slider data including the name and image for each slider.

    The `SliderModel` stores details related to each slider, which can be used in 
    various parts of the application like home pages or feature displays.

    Attributes:
        s_name (CharField): The name of the slider (e.g., "Banner", "Promotion").
        image (ImageField): The image associated with the slider.

    Methods:
        get_all_slider(): A static method that returns all the sliders stored in the database.
        __str__(): Returns the string representation of the slider object as the slider name.
    """
    s_name = models.CharField(max_length=50, null=True)
    image = CloudinaryField('slider')

    class Meta:
        db_table = "slider"
        # verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    @staticmethod
    def get_all_slider():
        """
        A static method to retrieve all the sliders stored in the database.

        Returns:
            QuerySet: A QuerySet containing all SliderModel instances.
        """
        return SliderModel.objects.all()

    def __str__(self):
        """
        Returns a string representation of the slider.

        This method outputs the slider as a string in the format:
        "{s_name}", where {s_name} is the name of the slider.

        Returns:
            str: A string representation of the slider.
        """
        return self.s_name
