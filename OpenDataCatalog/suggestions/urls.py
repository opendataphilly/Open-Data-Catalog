from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
   (r'^$', 'OpenDataCatalog.suggestions.views.list_all'),
   (r'^post/$', 'OpenDataCatalog.suggestions.views.add_suggestion'),
   (r'^vote/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.add_vote'),
   (r'^unvote/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.remove_vote'),
   (r'^close/(?P<suggestion_id>.*)/$', 'OpenDataCatalog.suggestions.views.close'),
)
