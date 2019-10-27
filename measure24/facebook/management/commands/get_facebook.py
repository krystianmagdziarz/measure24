# -*- coding: utf-8 -*-
from commons.facebook import Facebook
from django.core.management.base import BaseCommand, CommandError
from facebook.models import FacebookGroup, FacebookPost, FacebookPostCommentLvl0, FacebookPostCommentLvl1
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'Gets latest entries from facebook'

    def handle(self, *args, **options):
        facebook = Facebook("xoceanfirex@gmail.com", "Etq~CE(?(c7:T.<uaKY0z^YV}s=g,Deh", headless_mode=False)
        facebook.login()

        for group in FacebookGroup.objects.filter(active=True):
            facebook_entries = facebook.go_to_group(group.permalink)

            for entry in facebook_entries:
                # Dodanie postu
                post, created = FacebookPost.objects.get_or_create(
                    post_id=entry['post_id'],
                    message=entry['post_message'],
                    date=datetime.fromtimestamp(float(entry['post_date']), tz=pytz.UTC),
                    author=entry['post_author'],
                    permalink=entry['post_permalink'],
                    parent_group=group,
                )

                if entry['post_comments']:
                    # Dodanie komentarzy z lvl 0
                    for comment_lvl0 in entry['post_comments']:
                        comment, created_comment = FacebookPostCommentLvl0.objects.get_or_create(
                            comment_id=comment_lvl0['comment_id'],
                            author=comment_lvl0['author_name'],
                            link_profile=comment_lvl0['author_link_profile'],
                            date=datetime.fromtimestamp(float(comment_lvl0['comment_date']), tz=pytz.UTC),
                            message=comment_lvl0['comment_text'],
                            post=post
                        )

                        if comment_lvl0['subcomments']:
                            # Dodanie komentarzy z lvl 1
                            for comment_lvl1 in comment_lvl0['subcomments']:
                                comment1, created_lvl1 = FacebookPostCommentLvl1.objects.get_or_create(
                                    comment_id=comment_lvl1['comment_id'],
                                    author=comment_lvl1['author_name'],
                                    link_profile=comment_lvl1['author_link_profile'],
                                    date=datetime.fromtimestamp(float(comment_lvl1['comment_date']), tz=pytz.UTC),
                                    message=comment_lvl1['comment_text'],
                                    parent_group=comment,
                                )

        facebook.close()
