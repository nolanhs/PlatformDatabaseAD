from django.shortcuts import render, get_object_or_404, redirect
from .models import FundingEvent, Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from datetime import date

def funding_event_list(request):
    events = FundingEvent.objects.filter(end_date__gte=date.today())  # Only future/open events
    return render(request, 'funding/event_list.html', {'events': events})

def funding_event_detail(request, pk):
    event = get_object_or_404(FundingEvent, pk=pk)
    return render(request, 'funding/event_detail.html', {'event': event})

@login_required
def apply_for_event(request, pk):
    event = get_object_or_404(FundingEvent, pk=pk)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.event = event
            application.applicant = request.user
            application.save()
            return redirect('application_success')
    else:
        form = ApplicationForm()
    return render(request, 'funding/apply.html', {'form': form, 'event': event})