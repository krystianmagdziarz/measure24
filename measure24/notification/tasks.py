# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.mail import send_mail
from django.template.loader import render_to_string

from measure24.measure24.settings import EMAIL_USE_TLS
from measure24.commons.sentry import Sentry
from measure24.configuration.models import Configuration
from measure24.notification.models import Mentions

from celery import shared_task


@shared_task
def send_email():
    try:
        mentions = Mentions.objects.filter(used=False)

        if mentions.exists() and len(mentions) > 0:
            for mention in mentions:
                mention.used = True
                mention.save()

            msg_plain = render_to_string('email_text.txt', {'mentions': mentions})
            msg_html = render_to_string('email_html.html', {'mentions': mentions})

            if EMAIL_USE_TLS:
                config = Configuration.get_solo()
                if config.email_from and config.email_to:
                    send_mail(
                        'Wykryto słowa kluczowe',
                        msg_plain,
                        config.email_from,
                        [recipient for recipient in config.email_to.split(',')],
                        html_message=msg_html,
                        fail_silently=False,
                    )
            return len(mentions)
        return 0
    except Exception as ex:
        Sentry.capture_exception(ex)
