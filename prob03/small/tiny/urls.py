from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tiny.views',
    url(r'^\.json$', 'feed', name="tiny-feed"),
  )
