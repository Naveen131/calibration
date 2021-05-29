from django.db import models
from django.conf import settings
from accounts.models import Company
# Create your models here.
User= settings.AUTH_USER_MODEL




class Machines(models.Model):
    id = models.AutoField(primary_key=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE,db_column="company_name")
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="users")
    nomenclature = models.CharField(max_length=250,blank=False)
    certificate_number = models.TextField(max_length=250,blank=False)
    calibrated_date = models.DateField(blank=False)
    certificate_date = models.DateField(blank=False)
    expiry_date = models.DateField(blank=False)

    def __str__(self):
        return self.nomenclature
