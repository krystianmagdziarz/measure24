# -*- coding: utf-8 -*-
from commons.facebook import Facebook
from django.core.management.base import BaseCommand, CommandError
from facebook.models import FacebookGroup, FacebookPost, FacebookPostCommentLvl0, FacebookPostCommentLvl1


class Command(BaseCommand):
    help = 'Gets latest entries from facebook'

    def handle(self, *args, **options):
        facebook = Facebook("xoceanfirex@gmail.com", "Etq~CE(?(c7:T.<uaKY0z^YV}s=g,Deh", headless_mode=False)
        facebook.login()

        for group in FacebookGroup.objects.filter(active=True):
            facebook_entries = facebook.go_to_group(group.permalink)

            for entry in facebook_entries:
                # Dodanie postu
                post = FacebookPost()
                post.message = entry.post_message
                post.date = entry.post_date
                post.author = entry.post_author
                post.post_id = entry.post_id
                post.permalink = entry.post_permalink
                post.parent_group = group
                post.save()

                if entry.post_comments:
                    # Dodanie komentarzy z lvl 0
                    for comment_lvl0 in entry.post_comments:
                        comment = FacebookPostCommentLvl0()
                        comment.comment_id = comment_lvl0.comment_id
                        comment.author = comment_lvl0.author_name
                        comment.link_profile = comment_lvl0.author_link_profile
                        comment.date = comment_lvl0.comment_date
                        comment.message = comment_lvl0.comment_text
                        comment.post = post
                        comment.save()

                        if comment_lvl0.subcomments:
                            # Dodanie komentarzy z lvl 1
                            for comment_lvl1 in comment_lvl0.subcomments:
                                comment1 = FacebookPostCommentLvl1()
                                comment1.comment_id = comment_lvl1.comment_id
                                comment1.author = comment_lvl1.author_name
                                comment1.link_profile = comment_lvl1.author_link_profile
                                comment1.date = comment_lvl1.comment_date
                                comment1.message = comment_lvl1.comment_text
                                comment1.parent_group = comment
                                comment1.save()
