import nested_admin

from django.contrib import admin
from .models import FacebookPost, FacebookGroup, FacebookPostCommentLvl0, FacebookPostCommentLvl1


class CommentLvl1Inline(nested_admin.NestedStackedInline):
    model = FacebookPostCommentLvl1
    extra = 0
    fields = ['comment_id', 'author', 'message', 'date', 'link_profile']


class CommentLvl0Inline(nested_admin.NestedStackedInline):
    model = FacebookPostCommentLvl0
    extra = 0
    fields = ['comment_id', 'author', 'message', 'date', 'link_profile']
    inlines = [
        CommentLvl1Inline,
    ]


class FacebookLvl0(nested_admin.NestedModelAdmin):
    fields = ['comment_id', 'author', 'message', 'date', 'link_profile']


class FacebookLvl1(nested_admin.NestedModelAdmin):
    fields = ['comment_id', 'author', 'message', 'date', 'link_profile']


class FacebookPostAdmin(nested_admin.NestedModelAdmin):
    fields = ['post_id', 'author', 'message', 'date', 'permalink']
    inlines = [
        CommentLvl0Inline,
    ]


class FacebookGroupAdmin(nested_admin.NestedModelAdmin):
    fields = ['group_id', 'name', 'permalink', 'active']


admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(FacebookGroup, FacebookGroupAdmin)
admin.site.register(FacebookPostCommentLvl0, FacebookLvl0)
admin.site.register(FacebookPostCommentLvl1, FacebookLvl1)
