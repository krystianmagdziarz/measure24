# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from selenium.common.exceptions import NoSuchWindowException, TimeoutException

from measure24.facebook.models import FacebookGroup, FacebookPost, FacebookPostCommentLvl0, FacebookPostCommentLvl1, \
    FacebookUser
from measure24.commons.facebook import Facebook
from measure24.commons.sentry import Sentry

from celery import shared_task


@shared_task
def get_facebook():
    try:
        for user in FacebookUser.objects.all():
            facebook = Facebook(user.facebook_login, user.facebook_password, user.pk, headless_mode=False)
            facebook.login()

            try:
                for group in FacebookGroup.objects.filter(active=True, facebook_user=user):
                    facebook_entries = facebook.go_to_group(group.permalink)

                    for entry in facebook_entries:
                        # Dodanie postu
                        if not FacebookPost.objects.filter(post_id=entry['post_id']).exists():
                            post, created = FacebookPost.objects.get_or_create(
                                post_id=entry['post_id'],
                                message=entry['post_message'],
                                date=entry['post_date'],
                                author=entry['post_author'],
                                permalink=entry['post_permalink'],
                                parent_group=group,
                            )

                            if entry['post_comments'] and not \
                                    FacebookPostCommentLvl0.objects.filter(post_id=entry['comment_id']).exists():
                                # Dodanie komentarzy z lvl 0
                                for comment_lvl0 in entry['post_comments']:
                                    comment, created_comment = FacebookPostCommentLvl0.objects.get_or_create(
                                        comment_id=comment_lvl0['comment_id'],
                                        author=comment_lvl0['author_name'],
                                        link_profile=comment_lvl0['author_link_profile'],
                                        date=entry['post_date'],
                                        message=comment_lvl0['comment_text'],
                                        post=post,
                                    )

                                    if comment_lvl0['subcomments'] and not \
                                            FacebookPostCommentLvl1.objects.filter(post_id=entry['comment_id']).exists():
                                        # Dodanie komentarzy z lvl 1
                                        for comment_lvl1 in comment_lvl0['subcomments']:
                                            comment1, created_lvl1 = FacebookPostCommentLvl1.objects.get_or_create(
                                                comment_lvl0=comment,
                                                comment_id=comment_lvl1['comment_id'],
                                                author=comment_lvl1['author_name'],
                                                link_profile=comment_lvl1['author_link_profile'],
                                                date=entry['post_date'],
                                                message=comment_lvl1['comment_text'],
                                            )
                facebook.close()

            except TimeoutException as e:
                Sentry.capture_exception(e)
                facebook.close()
            except NoSuchWindowException as e:
                Sentry.capture_exception(e)
                facebook.close()
            except Exception as e:
                Sentry.capture_exception(e)
                facebook.close()
    except Exception as ex:
        Sentry.capture_exception(ex)
