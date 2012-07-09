from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
        (r'upload/$', 'warehouse.views.upload'),
        (r'postback/$', 'warehouse.views.postback'),
        (r'finalize/$', 'warehouse.views.finalize'),
)
