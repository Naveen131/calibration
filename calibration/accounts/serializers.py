from rest_framework import serializers
from .models import User
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .utils import account_activation_token
from django.urls import reverse
from machines.serializers import MachinesSerializer


def generate_activation_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key).encode('utf-8')).hexdigest()





class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    # email = serializers.EmailField(required=True)
    # user_name = serializers.CharField(required=True)
    # password = serializers.CharField(min_length=8, write_only=True)
    # date_of_birth

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        user = instance
        if password is not None:
            instance.set_password(password)
        instance.save()
        current_site = 'http://127.0.0.1:8000'
        email_body = {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
        }

        link = reverse('users:activate', kwargs={'uidb64': email_body['uid'], 'token': email_body['token']})

        email_subject = 'Activate your account'

        activate_url = current_site+link

        email = EmailMessage(
                    email_subject,
                    'Hi '+user.user_name + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [user.email],
                )
        email.send(fail_silently=False)
        return instance

# class UserViewSerializer(serializers.ModelSerializer):
#     machines = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
#     class Meta:
#         model = User
#         fields = ['username','machines']


class UserProfileSerilaizer(serializers.ModelSerializer):
    machines = MachinesSerializer()
    class Meta:
        model = User
        fields = ('email','username','date_of_birth')


class PasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=True
    )

    def validate_email(self, value):
        # Not validating email to have data privacy.
        # Otherwise, one can check if an email is already existing in database.
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):

    token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        uidb64, token = context.get('uidb64'), context.get('token')
        if uidb64 and token:
            uid = force_text(urlsafe_base64_decode(uidb64))
            self.user = self.get_user(uid)
            self.valid_attempt = self.token_generator.check_token(self.user, token)
        super(PasswordResetConfirmSerializer, self).__init__(*args, **kwargs)

    def get_user(self, uid):
        try:
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        label="New Password",
        write_only=True
    )

    new_password_2 = serializers.CharField(
        style={'input_type': 'password'},
        label="Confirm New Password",
        write_only=True
    )

    def validate_new_password_2(self, value):
        data = self.get_initial()
        new_password = data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def validate(self, data):
        if not self.valid_attempt:
            raise serializers.ValidationError("Operation not allowed.")
        return data
