from rest_framework import serializers
from .models import Machines


class MachinesSerializer(serializers.ModelSerializer):
    # company = serializers.RelatedField()
    class Meta:
        model = Machines
        fields = ('id','user','nomenclature','certificate_number' , 'calibrated_date','certificate_date','expiry_date')
