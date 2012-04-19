from opendata.models import Resource, DataType, Tag, CoordSystem, Url, UrlImage, Idea, IdeaImage
from suggestions.models import Suggestion
import simplejson as j

def tiny_resource_encoder(obj):
        return { "name" : obj.name,
                 "id" : obj.id,
                 "url" : "/api/resources/%s/" %(obj.id)
                 }


def short_resource_encoder(obj):
        return { "name" : obj.name,
                 "short_description" : obj.short_description,
                 "release_date" : obj.release_date,
                 "time_period" : obj.time_period,
                 "organization" : obj.organization,
                 "division" : obj.division,
                 "tags" : list(obj.tags.all()),

                 "area_of_interest" : obj.area_of_interest,
                 "is_published" : obj.is_published,
                 
                 "rating" : obj.rating.score,                 
               
                 "id" : obj.id,
                 "url" : "/api/resources/%s/" %(obj.id)
                 }

def full_resource_encoder(obj):
        return { "name" : obj.name,
                 "short_description" : obj.short_description,
                 "release_date" : obj.release_date,
                 "time_period" : obj.time_period,
                 "organization" : obj.organization,
                 "division" : obj.division,
                 "usage" : obj.usage,
                 "tags" : list(obj.tags.all()),
                 "data_types" : list(obj.data_types.all()),
                 "data_formats" : obj.data_formats,

                 "description" : obj.description,
                 "contact_phone" : obj.contact_phone,
                 "contact_email" : obj.contact_email,
                 "contact_url" : obj.contact_url,

                 "updates" : obj.updates.update_frequency if obj.updates else None,
                 "update_frequency" : obj.update_frequency,
                 "area_of_interest" : obj.area_of_interest,
                 "is_published" : obj.is_published,
                 
                 "created_by" : obj.created_by.username,
                 "last_updated_by" : obj.last_updated_by.username,
                 "last_updated" : obj.last_updated,
                 "metadata_contact" : obj.metadata_contact,
                 "metadata_notes" : obj.metadata_notes,

                 "coord_sys" : list(obj.coord_sys.all()),
                 "proj_coord_sys" : obj.proj_coord_sys,
                 "rating" : obj.rating.score,                 
               
                 "urls" : list(obj.url_set.all()),
                 "id" : obj.id
                 }

def encode_resource(resource_encoder):
    def encode_resource_with_encoder(obj):
        if isinstance(obj, Resource):
            return resource_encoder(obj)
        elif isinstance(obj, Suggestion):
            return { "text" : obj.text,
                     "suggested_by" : obj.suggested_by.username,
                     "suggested_date" : obj.suggested_date,
                     "last_modified_date" : obj.last_modified_date,
                     "rating" : obj.rating.votes,
                     "url" : "/api/suggestions/%s/" %(obj.id),
                     "id" : obj.pk
                     }
        elif isinstance(obj, Idea):
            return { "title" : obj.title,
                     "id" : obj.pk,
                     "description" : obj.description,
                     "author" : obj.author,
                     "created_by" : obj.created_by.username,
                     "created_by_date" : obj.created_by_date,
                     "updated_by" : obj.updated_by.username,
                     "updated_by_date" : obj.updated_by_date,
                     "resources" : list(obj.resources.all()),
                     "images" : list(IdeaImage.objects.filter(idea = obj).all())
                     }
        elif isinstance(obj, Url):
            return { "url" : obj.url,
                     "label" : obj.url_label,
                     "type" : obj.url_type.url_type,
                     "images" : list(obj.urlimage_set.all())
                     }            
        elif isinstance(obj, CoordSystem):
            return { "name": obj.name,
                     "description": obj.description,
                     "EPSG_code" : obj.EPSG_code
                     }
        elif isinstance(obj, UrlImage) or isinstance(obj, IdeaImage):
            return { "title" : obj.title,
                     "source" : obj.source,
                     "source_url" : obj.source_url,
                     "image_thumb_url" : "/media/" + obj.image.thumbnail.relative_url,
                     "image_url" : obj.image.url
                     }
        elif isinstance(obj, DataType):
            return obj.data_type
        elif isinstance(obj, Tag):
            return { "name" : obj.tag_name,
                     "url" : "/api/tags/%s/" % obj.tag_name }
        elif hasattr(obj, "strftime"):
            return obj.strftime("%Y-%m-%d")
        else:
            raise TypeError(repr(obj) + " is not JSON serializable")
    return encode_resource_with_encoder

def json_encode(obj, rsrc = short_resource_encoder):
    return j.dumps(obj, default = encode_resource(rsrc))

def json_load(jsonstr):
    return j.loads(jsonstr)
