from django.shortcuts import render
"""
I could use django-restframework or TastyPie, 
  but it's easier to emit dictionaries and you said
  you didn't want anything fancy. 

I'm foregoing implementing a syndication library, if you want
  an atom or rss protocol, just let me know and I'll make it 
  happen. ( https://docs.djangoproject.com/en/dev/ref/contrib/syndication/ )
"""

""" Algorithum
Create a small, working Django site that serves a simple activity feed list with 3 filters:
  1. My posts
  2. Me and the posts of everyone I'm tracking (note: use an asymmetric relationship, meaning, "Even if I track you, you may or may not track me".)
  3. Everybody's posts
"""
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from tiny.models import RegisteredUser, FeedItem

import json

class FeedItemEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, QuerySet):
      return [o for o in obj]

    if isinstance(obj, RegisteredUser):
      return obj.user.username

    if isinstance(obj, FeedItem):
      return {
        'content': mark_safe(force_unicode(obj.content).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')),
        'author': obj.user.username,
        'password': 'aoeu',
        'email': obj.user.email,
      }
    return super(FeedItemEncoder, self).default(obj)

def feed(request):
  following = RegisteredUser.objects.get(user=request.user).tracking.all()
  following_values = following.values_list('id', flat=True)
  FILTER_TYPES = {
    'm': lambda: FeedItem.objects.filter(user=request.user),
    # For time sake, I'm going to skip making this query optimal.
    'f': lambda: FeedItem.objects.filter(user__pk__in=following_values),
    'e': lambda: FeedItem.objects.all(), 
  }
  filter_type = request.GET.get('filterOn', FILTER_TYPES.keys()[0])
  if filter_type not in FILTER_TYPES.keys():
    filter_type = FILTER_TYPES.keys()[0]

  return HttpResponse(json.dumps({
    'status': 'OK',
    'data': {
      'following': following,
      'content': FILTER_TYPES.get(filter_type, 'e')(),
    }
  }, cls=FeedItemEncoder), content_type="application/json")

