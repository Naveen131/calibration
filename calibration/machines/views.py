from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.generics import RetrieveAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,DestroyAPIView
from rest_framework import generics,status,views
from .serializers import MachinesSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from rest_framework_simplejwt.backends import TokenBackend
from django.core.exceptions import ValidationError
from rest_framework import permissions
from .permissions import IsAdmin #IsOwnerOrAdmin
from .models import Machines

from django.shortcuts import render
# Create your views here.
class MachinesCreateView(CreateAPIView):
     serializer_class = MachinesSerializer
     authentication_class = JWTAuthentication
     permission_classes = [IsAdmin]
     queryset = Machines.objects.all()
     lookup_field = 'id'





     def post(self,request):
         user = self.request.user.pk
         print(user)

         serializer = self.serializer_class(data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()

         status_code = status.HTTP_201_CREATED

         response = {
                'success' :'True',
                'status_code':status_code,
                'message' :"machine added successfully"
         }
         return Response(response)


     def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE','POST']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]




class MachinesRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes =  [IsAuthenticated]
    queryset = Machines.objects.all()



class MachinesUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes =  [IsAdmin]
    #allowed_methods =['put','patch']
    lookup_field='id'
    queryset = Machines.objects.all()


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated successfully","details":serializer.data})

        else:
            return Response({"message": "failed", "details": serializer.errors})






class MachineDeleteView(generics.DestroyAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes =  [IsAdmin]
    lookup_field = 'id'
    queryset = Machines.objects.all()



class MachineListApi(ListAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes =  [IsAuthenticated]


    def get_queryset(self):
        if self.request.user.is_staff:
            return Machines.objects.all().order_by('-user')
        else:
            return Machines.objects.filter(user=self.request.user)
