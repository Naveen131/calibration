from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from calibration.celery import app
from machines.models import Machines
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives



REPORT_TEMPLATE = """
Here's how you did till now:

{% for machine in machines %}
        "{{ machines.expiry_date }}": viewed {{ machines.calibrated_date }} times |

{% endfor %}
"""


@app.task
def send_view_count_report():
    for machines in Machines.objects.all():
        x = machines.expiry_date - datetime.now().date()
        if x.days < 8:
            subject = 'Activate your account'
            message = "please Calibrate "

            msg = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, [machines.user.email])
            #msg.attach_alternative(message, "text/html")
            msg.send()
