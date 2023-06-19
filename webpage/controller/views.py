from django.shortcuts import render
from django.http import HttpResponse
# import HttpResponse
# Create your views here.
def index(request): 

    # return HttpResponse("test")

    return render(request, "index.html", {'name': 'Sakshee'})