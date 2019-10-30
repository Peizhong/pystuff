import logging
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

logger = logging.getLogger('django.middlewares')

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geo(ip):
    g = GeoIP2()
    try:
        city = g.city(ip)
        name = city['name']
        return city
    except AddressNotFoundError:
        return "AddressNotFound"
    return ""


class IPGeoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        ip = get_ip(request)
        city = get_geo(ip)
        vistor = "%s is from %s"%(ip,city)
        logger.debug(vistor)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response