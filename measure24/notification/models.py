from django.db import models
from django.core.mail import send_mail


class Words(models.Model):
    word = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = u"Monitorowane słowo"
        verbose_name_plural = u"Monitorowane słowa"


class NotificationAbstract(models.Model):
    message = models.TextField()

    def save(self, *args, **kwargs):

        for word in Words.objects.all():
            if str(word.word).lower() in str(self.message).lower():
                self.notify_on_email(word)

        super(NotificationAbstract, self).save(*args, **kwargs)

    def notify_on_email(self, Word, *args, **kwargs):
        send_mail(
            'Wykryto słowo %s' % Word.word,
            kwargs.get("message", "Nie przesłano treści"),
            'no-reply@meblezmetalu.pl',
            ['raport@meblezmetalu.pl'],
            fail_silently=False,
        )

    class Meta:
        abstract = True

