from django.http import HttpResponse


def spot(request, id):
    return HttpResponse("Spot %s" % id)

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow: /",
        content_type = 'text/plain'
    )
