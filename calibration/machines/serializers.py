from rest_framework import serializers
from .models import Machines,Company

class CompanySerializer(serializers.Serializer):
    class Meta:
        model = Company
        fields ='__all__'

class MachinesSerializer(serializers.ModelSerializer):
    # company = serializers.RelatedField()
    class Meta:
        model = Machines
        fields = ('id','user','nomenclature','company','certificate_number' , 'calibrated_date','certificate_date','expiry_date')
