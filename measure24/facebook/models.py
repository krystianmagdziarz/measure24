from django.db import models


class AbstractComment(models.Model):
    comment_id = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=50)
    message = models.TextField()
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


class FacebookPost(models.Model):
    parent_group = models.ForeignKey(FacebookGroup, blank=True, null=True, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    permalink = models.CharField(max_length=256)

    def __str__(self):
        return "%s - %s" % (self.author, self.date)


class FacebookPostCommentLvl0(AbstractComment):
    post = models.ForeignKey(FacebookPost, on_delete=models.CASCADE)


class FacebookPostCommentLvl1(AbstractComment):
    comment_lvl0 = models.ForeignKey(FacebookPostCommentLvl0, on_delete=models.CASCADE)
