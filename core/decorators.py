from django.http import HttpResponseForbidden
from functools import wraps

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You are not authorized to access this page.")
            user_groups = set(group.name for group in request.user.groups.all())
            if not user_groups.intersection(roles):
                return HttpResponseForbidden("You do not have the necessary permissions.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
