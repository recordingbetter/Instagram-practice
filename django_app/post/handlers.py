from corsheaders.signals import check_request_enabled

from .models import Post

def cors_allow_mysites(sender, request, **kwargs):
    return Post.objects.all()

check_request_enabled.connect(cors_allow_mysites)

def cors_allow_api_to_everyone(sender, request, **kwargs):
    return request.path.startswith('/post/')

check_request_enabled.connect(cors_allow_api_to_everyone)
