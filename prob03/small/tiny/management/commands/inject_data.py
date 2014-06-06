# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from optparse import make_option

from tiny.models import FeedItem, RegisteredUser

import feedparser
import random

User = get_user_model()

def bind_followers_to_ruid(ruid, followers):
  ruid = RegisteredUser.objects.get(pk=ruid)
  print ruid.user.username, followers
  followers = [RegisteredUser.objects.get(pk=fid) for fid in followers]
  ruid.tracking = followers
  ruid.save()

def get_or_create_registered_user(user):
  try:
    return RegisteredUser.objects.get(user=user)
  except RegisteredUser.DoesNotExist:
    ru = RegisteredUser.objects.create(user=user)
    return ru
def get_or_create_user(username):
  try:
    return User.objects.get(username=slugify(username))
  except User.DoesNotExist:
    user = User.objects.create(
      username=slugify(username),
      email='@'.join([slugify(username), 'jbcurtin.io']),
      )
    return user

class Command(BaseCommand):
  args = ""
  help = ""
  option_list = BaseCommand.option_list + (
    make_option('--randomize', 
      action="store_true", 
      dest="randomize", 
      default=False,
      help="This will destroy and create new random relationships"),
    )


  def handle(self, randomize=False, *args, **options):
    "Django fixtures are so finicky"
    for feed_uri in [
      'http://feeds.feedburner.com/RockPaperShotgun',
      'http://arrestedmotion.com/feed/',
    ]:
      feed = feedparser.parse(feed_uri)
      for entry in feed.entries:
        user = get_or_create_user(entry.get('author_detail').get('name'))
        user.is_staff = True
        user.is_superuser = True
        user.set_password('aoeu')
        user.save()
        ru = get_or_create_registered_user(user)
        feed_item = FeedItem.objects.create(
          user=user,
          content=entry.content[0]['value'][:1000])

    if randomize:
      registered_user_ids = RegisteredUser.objects.all().values_list('id', flat=True)
      def roll_dice(ruid_range):
        for uid in ruid_range:
          if random.randint(0,10) > 7:
            yield uid
      for ruid in registered_user_ids:
        followers = [f for f in roll_dice(registered_user_ids) if f != ruid]
        bind_followers_to_ruid(ruid, followers)



    
