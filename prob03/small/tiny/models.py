# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Ownable(models.Model):
  user = models.ForeignKey(User, 
    verbose_name=_("Author"), 
    related_name="%(class)ss", )
  class Meta: 
    abstract = True

  def __unicode__(self):
    return self.user

class RegisteredUser(models.Model):
  user = models.OneToOneField(User)
  tracking = models.ManyToManyField('self', 
    related_name='tracked_by',
    blank=True, 
    symmetrical=False, )

  def __unicode__(self):
    return "%s: %d" % (self.user, self.tracking.count())

class FeedItem(Ownable):
  content = models.CharField("Content", max_length=1000)

  def __unicode__(self):
    return "%s: %s..." % (self.user, self.content[:40])