from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def homepage(request):
    return HttpResponseRedirect(reverse("api:All games list"))