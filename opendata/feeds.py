from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed as Rss2
from django.shortcuts import get_object_or_404
from models import Resource, Tag, Idea

class BaseResourceFeed(Feed):
    feed_type = Rss2

    def item_title(self, item):
        return item.name
    def item_link(self, item):
        return item.get_absolute_url()
    def item_description(self, item):
        return item.short_description
    def item_author_name(self, item):
        return item.organization
    def item_author_email(self, item):
        return item.contact_email
    def item_author_link(self, item):
        return item.contact_url
    def item_categories(self, item):
        return item.tags.all()
    def item_pubdate(self, item):
        return item.created


class ResourcesFeed(BaseResourceFeed):
    title = "OpenDataPhilly.org: Resources - All"
    link = "/feeds/resources/"
    description = "List of resources on OpenDataPhilly.org listed in the order they were added"
    description_template = "feeds/resource.html"
    feed_type = Rss2

    def items(self):
        return Resource.objects.order_by('-created')
    
class UpdatesFeed(BaseResourceFeed):
    title = "OpenDataPhilly.org: Resources - Last Updated"
    link = "/feeds/updates/"
    description = "List of resources on OpenDataPhilly.org listed in the order they were last updated"
    description_template = "feeds/resource.html"
    feed_type = Rss2

    def items(self):
        return Resource.objects.order_by('-last_updated')
    
class IdeasFeed(Feed):
    title = "OpenDataPhilly.org: Ideas"
    link = "/feeds/ideas/"
    description = "List of ideas on OpenDataPhilly.org listed in the order they were added"
    description_template = "feeds/idea.html"
    feed_type = Rss2

    def items(self):
        return Idea.objects.order_by('-created_by_date')
    def item_title(self, item):
        return item.title
    def item_link(self, item):
        return item.get_absolute_url()
    def item_author_name(self, item):
        return item.author
    def item_description(self, item):
        return item.description

class TagFeed(BaseResourceFeed):
    description_template = "feeds/resource.html"
    
    def get_object(self, request, tag_id):
        return get_object_or_404(Tag, pk=tag_id)
    def title(self, obj):
        return "OpenDataPhilly.org: Resources in %s" % obj.tag_name
    def link(self, obj):
        return "/feeds/tag/%i" % obj.id
    def description(self, obj):
        return "Resources with the tag %s in the order they were added" % obj.tag_name

    def items(self, obj):
        return Resource.objects.filter(tags=obj).order_by('-created')
   
