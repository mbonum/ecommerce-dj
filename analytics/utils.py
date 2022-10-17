# from django.contrib.gis.utils import GeoIP


# def get_client_location(request):
#     g = GeoIP()
#     ip = get_client_ip(request)
#     if ip:
#         city = g.city(ip)['city']


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        _ip = x_forwarded_for.split(",")[0]
    else:
        _ip = request.META.get("REMOTE_ADDR", None)
        return _ip
