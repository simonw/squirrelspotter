from django.http import HttpResponse
from common.shortcuts import render

def index(request):
	return render(request, 'index.html')

def spot(request, id):
    return HttpResponse("Spot %s" % id)

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow: /",
        content_type = 'text/plain'
    )
