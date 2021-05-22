from django.shortcuts import render

# Create your views here.
from rest_framework import generics,status,views
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import generics, response, status, views
from .utils import account_activation_token,send_password_reset_email
from .models import User
#from .serializers import UserViewSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from machines.serializers import MachinesSerializer
from machines.permissions import IsAdmin
from machines.models import Machines


class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return self.is_valid(serializer)
        return self.is_invalid(serializer)


    def is_invalid(self, serializer):
        return response.Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def is_valid(self, serializer):
        user = serializer.save()
        # if not user.is_active:
        #     user.send_validation_email()
        #     ok_message = _(
        #         'Your account has been created and an activation link sent ' +
        #         'to your email address. Please check your email to continue.'
        #     )
        # else:
        #     ok_message = _('Your account has been created.')
        #
        return response.Response(
            data={'data': 'ok_message'},
            status=status.HTTP_201_CREATED,
        )


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# @api_view(('GET',))
# def activate(request,token):
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return Response('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return Response('Activation link is invalid!')


# class UserViewApi(generics.RetrieveAPIView):
#     serializer_class = UserViewSerializer()
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTTokenUserAuthentication]
#
#     def get_queryset(self):
#         print(self.request)
#         queryset=User.objects.get(pk=3)
#

class UserProfileAPI(generics.ListAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Machines.objects.filter(user=user)





class AdminProfileView(generics.ListAPIView,generics.CreateAPIView,generics.RetrieveAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    serializer_class = MachinesSerializer
    authentication_class = JWTAuthentication
    permission_classes = [IsAdmin]
    lookup_field = 'id'


    def get_queryset(self):
        return Machines.objects.all().order_by('-user')

    def get_object(self,pk):
        return Machines.objects.get(id=pk)

    def put(self,request,*args,**kwargs):
        id = self.request.data['id']
        obj = self.get_object(id)
        serializer = MachinesSerializer(obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                   'success' :'True',
                   'status_code':status_code,
                   'message' :"machine added successfully"
            }
            return Response(response)
        return Response({'status_code':status.HTTP_400_BAD_REQUEST,'message':"wrong parameter"})






class PasswordResetAPIView(views.APIView):

    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer


    def post(self,request):
        user = User.objects.get(email=request.data.get('email'))
        if user:
            send_password_reset_email(user,site='http://127.0.0.1:8000')
            return Response(status=status.HTTP_200_OK)
        return Response(status=statu.HTTP_200_OK)


class PasswordResetConfirmView(views.APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(
        data=request.data,
        context={
            'uidb64':kwargs['uidb64'],
            'token':kwargs['token']
        }
        )
        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data.get('new_password')
            user = serializer.user
            user.set_password(new_password)
            user.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)






class VerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # if not account_activation_token.check_token(user, token):
            #     return Response('User already activated')
            user.is_active = True
            user.save()

            # messages.success(request, 'Account activated successfully')
            return Response('Activated Successfully')
