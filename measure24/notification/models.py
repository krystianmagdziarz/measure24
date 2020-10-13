from django.db import models


class Words(models.Model):
    word = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = u"Monitorowane słowo"
        verbose_name_plural = u"Monitorowane słowa"


class Mentions(models.Model):
    word = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    permalink = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = u"Wzmianka"
        verbose_name_plural = u"Wzmianki"


class NotificationAbstract(models.Model):
    message = models.TextField()
    permalink = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):

        for word in Words.objects.all():
            if str(word.word).lower() in str(self.message).lower():
                mention = Mentions()
                mention.message = self.message
                mention.word = str(word.word)
                mention.permalink = self.permalink
                mention.save()

        super(NotificationAbstract, self).save(*args, **kwargs)

    class Meta:
        abstract = True

