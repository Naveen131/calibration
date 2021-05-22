from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

import datetime
import hashlib
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()




def send_password_reset_email(user, site):
        """
        Sends a password reset email to user.
        """

        context = {
            'email': user.email,
            'site': site,
            'site_name': getattr(settings, 'SITE_NAME', None),
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'user': user,
            'token': default_token_generator.make_token(user)
        }
        subject = render_to_string(
            'password_reset_email_subject.txt', context
        )

        subject = ''.join(subject.splitlines())

        message = render_to_string(
            'password_reset_email_content.txt', context
        )

        msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(message, "text/html")
        msg.send()
