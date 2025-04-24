from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.db.models import Q
from django.core.mail import send_mail
from datetime import date

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FundingEvent, Categorization, Profile, Application
from .forms import ApplicationForm, CustomUserCreationForm
from .serializers import (
    FundingEventSerializer,
    CategorizationSerializer,
    ProfileSerializer,
    ApplicationSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User


# ----------------- Forms ------------------
class EditProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False)
    organization = forms.CharField(max_length=255, required=False)


# ----------------- Views ------------------

def funding_event_list(request):
    query = request.GET.get('q')
    country = request.GET.get('country')
    events = FundingEvent.objects.all()
    today = date.today()
    for event in events:
        event.days_left = (event.end_date - today).days if event.end_date and event.end_date >= today else 0
    if query:
        events = events.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if country:
        events = events.filter(country__iexact=country)
    return render(request, 'funding/event_list.html', {
        'events': events,
        'today': date.today()
    })


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

            # Send confirmation email
            send_mail(
                subject=f"Application Submitted: {event.name}",
                message=f"Hi {request.user.username}, your application for '{event.name}' was submitted successfully.",
                from_email='no-reply@fundingplatform.com',
                recipient_list=[request.user.email],
                fail_silently=True,
            )

            messages.success(request, "Your application was submitted successfully.")
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
            messages.success(request, "Account created successfully! Welcome.")
            return redirect('dashboard')
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
            messages.success(request, "Your profile has been updated.")
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


@login_required
def dashboard_view(request):
    user_profile = request.user.profile
    recent_apps = Application.objects.filter(applicant=request.user).order_by('-submitted_at')[:5]
    total_apps = Application.objects.filter(applicant=request.user).count()
    return render(request, 'funding/dashboard.html', {
        'profile': user_profile,
        'recent_apps': recent_apps,
        'total_apps': total_apps,
    })


@login_required
def application_history(request):
    apps = Application.objects.filter(applicant=request.user)
    return render(request, 'funding/my_applications.html', {'apps': apps})


# ----------------- API Views ------------------

class ProtectedView(APIView):
    authentication_classes = []  # Fill in if using custom JWT setup
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This route is protected!"})


class FundingEventViewSet(viewsets.ModelViewSet):
    queryset = FundingEvent.objects.all()
    serializer_class = FundingEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategorizationViewSet(viewsets.ModelViewSet):
    queryset = Categorization.objects.all()
    serializer_class = CategorizationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
