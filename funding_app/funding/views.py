from django.shortcuts import render

# Create your views here.
# funding_app/views.py
from django.shortcuts import render
from .models import FundingEvent

def index(request):
    return render(request, 'funding_app/index.html')

def funding_events(request):
    events = FundingEvent.objects.all()
    return render(request, 'funding_app/events.html', {'events': events})