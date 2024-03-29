from django.core.exceptions import ValidationError
from django.db import models
from measure24.notification.models import NotificationAbstract


class FacebookUser(models.Model):
    facebook_login = models.CharField(max_length=50, null=False, blank=False)
    facebook_password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return "%s" % self.facebook_login

    class Meta:
        verbose_name = "Konto Facebook"
        verbose_name_plural = "Konta Facebook"


class AbstractComment(NotificationAbstract):
    comment_id = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    link_profile = models.CharField(max_length=256)

    def __str__(self):
        return "%s - %s" % (self.author, self.message)

    class Meta:
        abstract = True


class FacebookGroup(models.Model):
    facebook_user = models.ForeignKey(FacebookUser, null=False, on_delete=models.CASCADE,
                                      help_text="Użytkownik z prawem dostępu do grupy")
    name = models.CharField(max_length=100, null=True, blank=True, help_text="Nazwa w systemie")
    permalink = models.CharField(max_length=256, help_text="Adres lub ID grupy")
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Grupa - %s" % self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if "http" not in self.permalink and "https" not in self.permalink:
            if len(self.permalink) > 0:
                if self.permalink[0] == "/":
                    self.permalink = self.permalink[1:]
                elif self.permalink[-1:] == "/":
                    self.permalink = self.permalink[:-1]

            self.permalink = "https://www.facebook.com/groups/%s/" % self.permalink

        super(FacebookGroup, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    class Meta:
        verbose_name = "Grupa"
        verbose_name_plural = "Grupy"


class FacebookPost(NotificationAbstract):
    parent_group = models.ForeignKey(FacebookGroup, blank=True, null=True, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=50)
    date = models.CharField(null=True, blank=True, max_length=120)

    def __str__(self):
        return "%s - %s" % (self.author, self.message)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"


class FacebookPostCommentLvl0(AbstractComment):
    post = models.ForeignKey(FacebookPost, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"


class FacebookPostCommentLvl1(AbstractComment):
    comment_lvl0 = models.ForeignKey(FacebookPostCommentLvl0, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Odpowiedź do komentarza"
        verbose_name_plural = "Odpowiedzi do komentarzy"
