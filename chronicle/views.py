from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html', {
        'new_sess_text': request.POST.get('sess_text', ''),
    })


