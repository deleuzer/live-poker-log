from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return HttpResponse('<html><title>Poker Chronicle</title></html>')

