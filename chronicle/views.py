from django.shortcuts import redirect, render

from chronicle.models import PokerSession

def home_page(request):
    if request.method == 'POST':
        PokerSession.objects.create(text=request.POST['sess_text'])
        return redirect('/chronicles/the-only-session-in-the-world/')
    chronicles = PokerSession.objects.all()
    return render(request, 'home.html', {'chronicles': chronicles})

def view_chronicles(request):
    chronicles = PokerSession.objects.all()
    return render(request, 'chronicles.html', {'chronicles': chronicles})

