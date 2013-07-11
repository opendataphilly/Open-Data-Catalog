from OpenDataCatalog.comments.models import CommentWithRating
from OpenDataCatalog.comments.forms import CommentFormWithRating

def get_model():
    return CommentWithRating

def get_form():
    return CommentFormWithRating
