from django.db import models
from django.conf import settings
# Create your models here.
User= settings.AUTH_USER_MODEL




class Machines(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    nomenclature = models.CharField(max_length=250,blank=False)
    certificate_number = models.TextField(max_length=250,blank=False)
    calibrated_date = models.DateField(blank=False)
    certificate_date = models.DateField(blank=False)
    expiry_date = models.DateField(blank=False)

    def __str__(self):
        return self.nomenclature
