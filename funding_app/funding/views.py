from django.shortcuts import render, get_object_or_404, redirect
from .models import FundingEvent, Application, Profile
from .forms import ApplicationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth import login
from django import forms
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import FundingEvent, Categorization, Profile, Application
from .serializers import (
    FundingEventSerializer,
    CategorizationSerializer,
    ProfileSerializer,
    ApplicationSerializer,
    UserSerializer,
)

class EditProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20, required=False)
    age = forms.IntegerField(required=False)
    organization = forms.CharField(max_length=255, required=False)

def funding_event_list(request):
    events = FundingEvent.objects.all()
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

class ProtectedView(APIView):
    authentication_classes = [  ]  # This specifies that JWT Authentication should be used
    permission_classes = [IsAuthenticated]       # This specifies that only authenticated users are allowed

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