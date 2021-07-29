from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.urls import resolve
from django.utils.module_loading import import_string
from netaddr import IPAddress, IPSet

DEFAULT_GETTER = 'core.middleware.get_remote_addr'


def get_remote_addr(request):
    return request.META['REMOTE_ADDR']


def get_ipaddr(request):
    path = getattr(settings, 'ADMIN_IP_GETTER', DEFAULT_GETTER)
    func = import_string(path)
    return IPAddress(func(request))


def get_ipset_from_settings(name):
    return IPSet(getattr(settings, name, []))


class AdminWhitelistMiddleware:
    """Limits login to specific IP's in Django 3"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_url = resolve(request.path_info)
        is_admin_app = (current_url.app_name == 'admin')
        whitelist = get_ipset_from_settings('ADMIN_WHITELIST')
        if is_admin_app and not get_ipaddr(request) in whitelist:
            raise PermissionDenied
        return self.get_response(request)
