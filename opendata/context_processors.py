from django.conf import settings


def get_current_path(request):
    return {'current_path': request.get_full_path(), 'current_host': request.get_host()}

def get_settings(request):
    return {'SITE_ROOT': settings.SITE_ROOT}

