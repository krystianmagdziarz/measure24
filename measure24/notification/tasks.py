# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.mail import send_mail

from measure24.measure24.settings import EMAIL_USE_TLS
from measure24.commons.sentry import Sentry
from measure24.configuration.models import Configuration

from celery import shared_task


@shared_task
def send_email():
    try:
        if EMAIL_USE_TLS:
            config = Configuration.get_solo()
            if config.email_from and config.email_to:
                send_mail(
                    'Wykryto słowo %s' % Word.word,
                    kwargs.get("message", "Nie przesłano treści"),
                    config.email_from,
                    [recipient for recipient in config.email_to.split(',')],
                    fail_silently=False,
                )
    except Exception as ex:
        Sentry.capture_exception(ex)
