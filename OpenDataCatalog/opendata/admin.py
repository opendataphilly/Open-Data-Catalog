from datetime import datetime
from opendata.models import *
from comments.models import *
from suggestions.models import *
from contest.models import *
from django.contrib import admin

class UrlImageInline(admin.TabularInline):
    model = UrlImage
    extra = 1
    
class UrlInline(admin.TabularInline):
    model = Url
    extra = 1
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'

class IdeaImageInline(admin.TabularInline):
    model = IdeaImage
    extra = 1

class ResourceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('name', 'is_published'), 'description', 'short_description', 'usage', 
            ('organization', 'division'), ('contact_phone', 'contact_email', 'contact_url')], 'classes':['wide']}),
        ('Metadata Fields ', {'fields':['release_date', ('time_period', 'update_frequency'), 
            'updates',
            ('data_formats', 'area_of_interest'), 'proj_coord_sys', 
            ('created_by', 'created'), ('last_updated_by', 'last_updated'),
            'metadata_contact','metadata_notes', 'data_types', 'coord_sys', 'tags', ], 'classes':['wide']})
    ]
    readonly_fields = ['created_by', 'created', 'last_updated_by', 'last_updated']
    inlines = [UrlInline,]
    
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'
    list_display = ('name', 'organization', 'release_date', 'is_published')
    search_fields = ['name', 'description', 'organization']
    list_filter = ['tags', 'url__url_type', 'is_published']
    date_heirarchy = 'release_date'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created = datetime.now()
        
        obj.last_updated_by = request.user
        obj.save()

class UrlImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ['image', 'title', 'description']
    
class UrlAdmin(admin.ModelAdmin):
    list_display = ('url_label', 'url_type', 'url')
    inlines = [UrlImageInline,]
    list_filter = ['url_type',]
    
class CoordSystemAdmin(admin.ModelAdmin):
    list_display = ('EPSG_code', 'name')
    search_fields = ['name', 'EPSG_code', 'description']

    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls'
class IdeaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':[('title', 'author'),  'description', ('created_by', 'created_by_date'), 
                ('updated_by', 'updated_by_date'), 'resources']})
    ]
    readonly_fields = ['created_by', 'created_by_date', 'updated_by', 'updated_by_date']
    inlines = [IdeaImageInline, ]

    list_display = ('title', 'created_by', 'created_by_date', 'updated_by', 'updated_by_date')
    search_fields = ['title',]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.created_by_date = datetime.now()
        
        obj.updated_by = request.user
        obj.save()

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'suggested_by', 'completed']
    search_fields = ['text', 'suggested_by']

class SubmissionAdmin(admin.ModelAdmin):   
    verbose_name = 'Resource Url'
    verbose_name_plural = 'Resource Urls' 
    list_display = ['user', 'sent_date']
    search_fields = ['email_text', 'user']
    readonly_fields = ['user',]

class ODPUserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'can_notify',]
    fieldsets = [(None, {'fields':['user', 'organization', 'can_notify']}),]
    readonly_fields = ['user',]
    list_filter = ['can_notify',]
    
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'nominator', 'contest']
    search_fields = ['title', 'nominator', 'description']
    list_filter = ['contest__title', ]

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1
    verbose_name_plural = 'Entries'

class ContestAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date']
    search_fields = ['title', 'rules']
    inlines = [EntryInline, ]

class VoteAdmin(admin.ModelAdmin):
    list_display= ['entry', 'user', 'timestamp']
    search_fields = ['entry']
    list_filter = ['entry',]

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ODPUserProfile, ODPUserProfileAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(IdeaImage)
admin.site.register(Tag)
admin.site.register(UpdateFrequency)
admin.site.register(UrlType)
admin.site.register(CoordSystem, CoordSystemAdmin)
admin.site.register(DataType)
admin.site.register(Url, UrlAdmin)
admin.site.register(UrlImage, UrlImageAdmin)
admin.site.register(Resource, ResourceAdmin)

admin.site.register(Contest, ContestAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Vote, VoteAdmin)

admin.site.register(CommentWithRating)

