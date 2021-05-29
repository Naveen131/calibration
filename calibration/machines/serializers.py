from rest_framework import serializers
from .models import Machines


class MachinesSerializer(serializers.ModelSerializer):
    # company = serializers.StringRelatedField()
    #user = serializers.StringRelatedField()

    class Meta:
        model = Machines
        fields = ('id','user','company','nomenclature','certificate_number' , 'calibrated_date','certificate_date','expiry_date')
