from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .celery import app
from machines.models import Machines
from datetime import date

REPORT_TEMPLATE = """
Here's how you did till now:

{% for machine in machines %}
        "{{ machines.expiry_date }}": viewed {{ machines.calibrated_date }} times |

{% endfor %}
"""


@app.task
def send_view_count_report():
    for machines in Machines.objects.all():
        if datetime.now().date() - machines.expiry_date() == 7:
            template = Template(REPORT_TEMPLATE)
            send_mail(
            'Your QuickPublisher Activity',
            template.render(context=Context({'machines': machines})),
            'from@quickpublisher.dev',
            [machines.user.email],
            fail_silently=False,)
