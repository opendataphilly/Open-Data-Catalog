from comments.models import CommentWithRating
from comments.forms import CommentFormWithRating

def get_model():
    return CommentWithRating

def get_form():
    return CommentFormWithRating
