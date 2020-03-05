# -*- coding: utf-8 -*-
from commons.facebook import Facebook
from django.core.management.base import BaseCommand, CommandError
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from facebook.models import FacebookGroup, FacebookPost, FacebookPostCommentLvl0, FacebookPostCommentLvl1, FacebookUser
from datetime import datetime
from commons.sentry import Sentry
import pytz


class Command(BaseCommand):
    help = 'Gets latest entries from facebook'

    def handle(self, *args, **options):

        for user in FacebookUser.objects.all():
            facebook = Facebook(user.facebook_login, user.facebook_password, user.pk, headless_mode=False)
            facebook.login()

            try:
                for group in FacebookGroup.objects.filter(active=True, facebook_user=user):
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
                                    post=post,
                                )

                                if comment_lvl0['subcomments']:
                                    # Dodanie komentarzy z lvl 1
                                    for comment_lvl1 in comment_lvl0['subcomments']:
                                        comment1, created_lvl1 = FacebookPostCommentLvl1.objects.get_or_create(
                                            comment_lvl0=comment,
                                            comment_id=comment_lvl1['comment_id'],
                                            author=comment_lvl1['author_name'],
                                            link_profile=comment_lvl1['author_link_profile'],
                                            date=datetime.fromtimestamp(float(comment_lvl1['comment_date']), tz=pytz.UTC),
                                            message=comment_lvl1['comment_text'],
                                        )
                facebook.close()

            except TimeoutException:
                facebook.close()
            except NoSuchWindowException:
                facebook.close()
            except Exception as e:
                Sentry.capture_exception(e)
                facebook.close()
