from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
import boto3


def create_token():
    rand_token = uuid4()
    return rand_token

def send_mail(to, template, context):
    html_content = render_to_string(f'{template}.html', context)
    text_content = render_to_string(f'{template}.txt', context)

    msg = EmailMultiAlternatives(context['subject'], text_content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def send_activation_email(request, email, code):
    context = {
        'subject': _('Profile activation'),
        'uri': request.build_absolute_uri(reverse('activate', kwargs={'code': code})),
    }

    send_mail(email, 'activate_profile', context)


def send_activation_change_email(request, email, code):
    context = {
        'subject': _('Change email'),
        'uri': request.build_absolute_uri(reverse('change_email_activation', kwargs={'code': code})),
    }

    send_mail(email, 'change_email', context)


def send_reset_password_email(request, email, token, uid):
    context = {
        'subject': _('Restore password'),
        'uri': request.build_absolute_uri(
            reverse('restore_password_confirm', kwargs={'uidb64': uid, 'token': token})),
    }

    send_mail(email, 'restore_password_email', context)


def send_forgotten_username_email(email, username):
    context = {
        'subject': _('Your username'),
        'username': username,
    }

    send_mail(email, 'forgotten_username', context)

def send_email(to, subject, body):
    region_name = 'us-east-1'
    ses = boto3.client('ses', region_name=region_name)

    # Sender and recipient email addresses
    sender_email = 'htusharmatta96@gmail.com'
    recipient_email = to

    # Create the email message
    message = {
        'Subject': {'Data': subject},
        'Body': {'Text': {'Data': body}}
    }
    response = ses.send_email(
        Source=sender_email,
        Destination={'ToAddresses': [recipient_email]},
        Message=message
    )


def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff