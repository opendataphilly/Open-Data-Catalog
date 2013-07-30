from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.conf import settings
from django.conf.urls.static import static

from OpenDataCatalog.opendata.feeds import ResourcesFeed, TagFeed, IdeasFeed, UpdatesFeed
from OpenDataCatalog.opendata.models import Resource, Idea
from OpenDataCatalog.registration_backend import CatalogRegistrationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {
    'flatpages': FlatPageSitemap,
    'resources': GenericSitemap({'queryset': Resource.objects.all(), 'date_field': 'created'}, priority=0.5),
    'ideas': GenericSitemap({'queryset': Idea.objects.all(), 'date_field': 'created_by_date'}, priority=0.5),
}

urlpatterns = patterns('',
    # Examples:
    (r'^$', 'OpenDataCatalog.opendata.views.home'),
    (r'^opendata/$', 'OpenDataCatalog.opendata.views.results'),
    
    (r'^opendata/tag/(?P<tag_id>\d+)/$', 'OpenDataCatalog.opendata.views.tag_results'),
    (r'^opendata/search/$', 'OpenDataCatalog.opendata.views.search_results'),
    (r'^opendata/resource/(?P<resource_id>\d+)/$', 'OpenDataCatalog.opendata.views.resource_details'),
    (r'^opendata/resource/(?P<resource_id>\d+)/(?P<slug>[-\w]+)/$', 'OpenDataCatalog.opendata.views.resource_details'),
    (r'^ideas/$', 'OpenDataCatalog.opendata.views.idea_results'),
    (r'^idea/(?P<idea_id>\d+)/$', 'OpenDataCatalog.opendata.views.idea_results'),
    (r'^idea/(?P<idea_id>\d+)/(?P<slug>[-\w]+)/$', 'OpenDataCatalog.opendata.views.idea_results'),
    (r'^opendata/submit/$', 'OpenDataCatalog.opendata.views.suggest_content'),
    (r'^thanks/$', 'OpenDataCatalog.opendata.views.thanks'),   
    
    (r'^tags/$', 'OpenDataCatalog.opendata.views.get_tag_list'),
    
    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^accounts/register/$', CatalogRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/password_reset', 'django.contrib.auth.views.password_reset'),
    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^opendata/nominate/', include('OpenDataCatalog.suggestions.urls')),

    (r'^contest/$', 'OpenDataCatalog.contest.views.get_entries'),
    (r'^contest/rules/$', 'OpenDataCatalog.contest.views.get_rules'),
    (r'^contest/add/$', 'OpenDataCatalog.contest.views.add_entry'),
    (r'^contest/entry/(?P<entry_id>\d+)/$', 'OpenDataCatalog.contest.views.get_entry'),
    (r'^contest/entry/(?P<entry_id>\d+)/vote/$', 'OpenDataCatalog.contest.views.add_vote'),
    (r'^contest/entries/$', 'OpenDataCatalog.contest.views.get_entries_table'),
    (r'^contest/winners/$', 'OpenDataCatalog.contest.views.get_winners'),

    (r'^feeds/$', 'OpenDataCatalog.opendata.views.feed_list'),
    (r'^feeds/resources/$', ResourcesFeed()),
    (r'^feeds/updates/$', UpdatesFeed()),
    (r'^feeds/ideas/$', IdeasFeed()),
    (r'^feeds/tag/(?P<tag_id>\d+)/$', TagFeed()),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    
    # API urls (all are GET urls unless stated otherwise)
    (r'^api/resources/$', 'OpenDataCatalog.api.views.resources'),
    (r'^api/resources/(?P<resource_id>\d+)/$', 'OpenDataCatalog.api.views.resource'),                 
    (r'^api/resources/search$', 'OpenDataCatalog.api.views.resource_search'),
    (r'^api/tags/$', 'OpenDataCatalog.api.views.tags'),                       
    (r'^api/tags/(?P<tag_name>.*)/$', 'OpenDataCatalog.api.views.by_tag'),
    (r'^api/ideas/$', 'OpenDataCatalog.api.views.ideas'),
    (r'^api/ideas/(?P<idea_id>\d+)/$', 'OpenDataCatalog.api.views.idea'),
    # GET to list, POST to created
    (r'^api/suggestions/$', 'OpenDataCatalog.api.views.suggestions'),
    (r'^api/suggestions/search$', 'OpenDataCatalog.api.views.search_suggestions'),
    (r'^api/suggestions/(?P<suggestion_id>\d+)/$', 'OpenDataCatalog.api.views.suggestion'),
    # PUT to vote, DELETE to remove
    (r'^api/suggestions/(?P<suggestion_id>\d+)/vote$', 'OpenDataCatalog.api.views.vote'),
    # POST to create
    (r'^api/submit/$', 'OpenDataCatalog.api.views.submit'),

    url(r'^catalog/', include("OpenDataCatalog.catalog.urls")),

    # Uncomment the next line to enable the admin:
    url(r'^_admin_/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
