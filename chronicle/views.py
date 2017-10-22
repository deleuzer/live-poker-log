from django.shortcuts import redirect, render

from chronicle.models import PokerSession, Chronicles

def home_page(request):
    return render(request, 'home.html')

def view_chronicles(request, chronicles_id):
    chronicles = Chronicles.objects.get(id=chronicles_id)
    return render(request, 'chronicles.html', {'chronicles': chronicles})

def new_chronicle(request):
    chronicles = Chronicles.objects.create()
    PokerSession.objects.create(text=request.POST['sess_text'], chronicles=chronicles)
    return redirect(f'/chronicles/{chronicles.id}/')

def add_sess(request, chronicle_id):
    chronicles = Chronicles.objects.get(id=chronicle_id)
    PokerSession.objects.create(text=request.POST['sess_text'], chronicles=chronicles)
    return redirect(f'/chronicles/{chronicles.id}/')



