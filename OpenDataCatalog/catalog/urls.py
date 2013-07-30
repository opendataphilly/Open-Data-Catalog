from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^csw$','OpenDataCatalog.catalog.views.csw'),
)
