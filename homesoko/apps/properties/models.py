from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import HStoreField
from homesoko.apps.core.model_utils import ChoiceEnum


class City(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    name = models.CharField(max_length=100, blank=False)
    city = models.ForeignKey(City, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}".format(self.name, self.city)


class Property(models.Model):

    class Categories(ChoiceEnum):
        LETTING = 'Letting'
        FOR_SALE = 'For Sale'

    class PropertyTypes(ChoiceEnum):
        APARTMENT = 'Apartment'
        HOUSE = 'House'
        OFFICE = 'Office'
        LAND = 'Land'
        TOWNHOUSE = 'Townhouse'

    class Bedrooms(ChoiceEnum):
        ALL_ENSUITE = 'All Ensuite'
        ONE = '1'
        TWO = '2'
        THREE = '3'
        FOUR = '4'
        FIVE = '5'
        SIX = '6'
        SEVEN = '7'

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    description = models.TextField(blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.CharField(max_length=20, blank=True, choices=Bedrooms.choices())
    structure_size = models.PositiveIntegerField(null=True, blank=True, help_text='Size of the structure in square feet')
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, null=False, blank=False, related_name='properties', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Categories.choices())
    property_type = models.CharField(max_length=50, choices=PropertyTypes.choices())
    features = HStoreField(default={})
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Properties'


class PropertyImage(models.Model):
    image = models.ImageField()
    related_property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, blank=True)
