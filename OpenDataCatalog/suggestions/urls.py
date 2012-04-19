from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
   (r'^$', 'suggestions.views.list_all'),
   (r'^post/$', 'suggestions.views.add_suggestion'),
   (r'^vote/(?P<suggestion_id>.*)/$', 'suggestions.views.add_vote'),
   (r'^unvote/(?P<suggestion_id>.*)/$', 'suggestions.views.remove_vote'),
   (r'^close/(?P<suggestion_id>.*)/$', 'suggestions.views.close'),
)
