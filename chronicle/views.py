from django.shortcuts import redirect, render

from chronicle.models import PokerSession

def home_page(request):
    return render(request, 'home.html')

def view_chronicles(request):
    chronicles = PokerSession.objects.all()
    return render(request, 'chronicles.html', {'chronicles': chronicles})

def new_chronicle(request):
    PokerSession.objects.create(text=request.POST['sess_text'])
    return redirect('/chronicles/the-only-session-in-the-world/')


