from django.db import models
from solo.models import SingletonModel


class Configuration(SingletonModel):
    name = models.CharField(u"Nazwa", null=False, default=u"Domyślna konfiguracja", max_length=100, )
    active = models.BooleanField(u"Włączony", null=False, default=True)
    sentry_sdk = models.CharField(u"Sentry URL", null=True, blank=True, max_length=200,
                                  help_text="https://23ac1c5dc1ad4233a5176af52bdc3aaa@sentry.io/2035970")
    max_entry = models.IntegerField(u"Max wpisów", null=False, default=10,
                                    help_text="Maksymalna liczba przeglądanych postów z wall-a konkretnej grupy")
    email_from = models.CharField(u"E-mail nadawcy", null=False, default="no-reply@kmagdziarz.pl", max_length=100,
                                  help_text="Adres e-mail nadawcy raportu")
    email_to = models.CharField(u"E-mail odbiorcy", null=False, default="raport@kmagdziarz.pl", max_length=100,
                                help_text="Adres e-mail odbiorcy raportu")
    capture_event = models.BooleanField(u"Sentry capture event", null=False, default=False,
                                        help_text="Zbieraj także powiadomienia o wszystkich event logach")

    def __str__(self):
        return "Ustawienia: %s" % self.name

    class Meta:
        verbose_name = u'Konfiguracja strony'
        verbose_name_plural = u'Konfiguracje strony'

