from datetime import timedelta
from django.db import models

# Create your models here.

from django.db import models

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=255)
    features = models.TextField()
    image = models.ImageField(upload_to='property_images',null=True,default='no-property-photo.jpg')

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.name

    

class Unit(models.Model):
    name = models.CharField(max_length=100, default='flat',null=True,blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('1BHK', '1BHK'), ('2BHK', '2BHK'), ('3BHK', '3BHK'), ('4BHK', '4BHK')])
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    features = models.TextField()

    def __str__(self):
        return self.name

class Tenant(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    monthly_rent_date = models.DateField()
    lease_expiry_date = models.DateField()
    document_proof = models.FileField(upload_to='document_proof/',null=True, blank=True)
    def __str__(self):
        return self.name
    



