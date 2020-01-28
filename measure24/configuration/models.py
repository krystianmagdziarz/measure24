from django.db import models


class Configuration(models.Model):
    name = models.CharField(u"Nazwa", null=False, default=u"Domyślna konfiguracja", max_length=100, )
    active = models.BooleanField(u"Włączony", null=False, default=True)
    sentry_sdk = models.CharField(u"Sentry URL", null=True, blank=True, max_length=200,
                                  help_text="https://23ac1c5dc1ad4233a5176af52bdc3aaa@sentry.io/2035970")

    def __str__(self):
        return "Ustawienia: %s" % self.name

    class Meta:
        verbose_name = u'Konfiguracja strony'
        verbose_name_plural = u'Konfiguracje strony'

