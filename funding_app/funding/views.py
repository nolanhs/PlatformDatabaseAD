from django.shortcuts import render, get_object_or_404, redirect
from .models import FundingEvent, Application, Profile
from .forms import ApplicationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import login
from django import forms

class EditProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False)
    organization = forms.CharField(max_length=255, required=False)

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

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list')  # Redirect to your event list
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile.full_name = form.cleaned_data["full_name"]
            profile.email = form.cleaned_data["email"]
            profile.phone_number = form.cleaned_data.get("phone_number")
            profile.age = form.cleaned_data.get("age")
            profile.organization = form.cleaned_data.get("organization")
            profile.save()
            return redirect('event_list')
    else:
        form = EditProfileForm(initial={
            "full_name": profile.full_name,
            "email": profile.email,
            "phone_number": profile.phone_number,
            "age": profile.age,
            "organization": profile.organization
        })

    return render(request, 'funding/edit_profile.html', {
        'form': form,
        'profile': profile
    })