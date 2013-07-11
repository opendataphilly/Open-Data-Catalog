from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^csw$','OpenDataCatalog.catalog.views.csw'),
)
