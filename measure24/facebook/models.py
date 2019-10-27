from django.db import models
from notification.models import NotificationAbstract


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
    group_id = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    permalink = models.CharField(max_length=256)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Grupa - %s" % self.name


class FacebookPost(NotificationAbstract):
    parent_group = models.ForeignKey(FacebookGroup, blank=True, null=True, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=50)
    date = models.DateTimeField(null=True, blank=True)
    permalink = models.CharField(max_length=256)

    def notify_on_email(self, Word, *args, **kwargs):
        message = "Grupa: %s\r\n\r\nWykryto słowo: %s w poście, %s autorstwa %s " % \
                  (self.parent_group.name, Word, self.permalink, self.author)
        super(FacebookPost, self).notify_on_email(Word, message=message, *args, **kwargs)

    def __str__(self):
        return "%s - %s" % (self.author, self.message)


class FacebookPostCommentLvl0(AbstractComment):
    post = models.ForeignKey(FacebookPost, on_delete=models.CASCADE)

    def notify_on_email(self, Word, *args, **kwargs):
        message = "Grupa: %s\r\n\r\nWykryto słowo: %s w komentarzu lvl0, %s autorstwa %s " % \
                  (self.post.parent_group.name, Word, self.post.permalink, self.author)
        super(FacebookPostCommentLvl0, self).notify_on_email(Word, message=message, *args, **kwargs)


class FacebookPostCommentLvl1(AbstractComment):
    comment_lvl0 = models.ForeignKey(FacebookPostCommentLvl0, on_delete=models.CASCADE)

    def notify_on_email(self, Word, *args, **kwargs):
        message = "Grupa: %s\r\n\r\nWykryto słowo: %s w komentarzu lvl1, %s autorstwa %s, który dotyczy komentarza %s " % \
               (self.comment_lvl0.post.parent_group.name, Word,
                self.comment_lvl0.post.permalink, self.author, self.comment_lvl0.author)
        super(FacebookPostCommentLvl1, self).notify_on_email(Word, message=message, *args, **kwargs)
