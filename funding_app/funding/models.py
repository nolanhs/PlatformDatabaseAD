from django.db import models
from django.contrib.auth.models import User

class FundingEvent(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    location = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    funder = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Categorization(models.Model):
    FUNDING_TYPES = [
        ('Seed', 'Seed'),
        ('Series A', 'Series A'),
        ('Series B', 'Series B'),
    ]

    funding_type = models.CharField(max_length=50, choices=FUNDING_TYPES)
    industry_fields = models.CharField(max_length=255)  
    eligibility_criteria = models.TextField(blank=True, null=True)
    is_open_round = models.BooleanField(default=True)
    application_deadline = models.DateField(blank=True, null=True)

    event = models.OneToOneField(FundingEvent, on_delete=models.CASCADE, related_name="categorization")

    def __str__(self):
        return f"{self.funding_type} - {self.event.name}"

class User(models.Model):
    USER_ROLES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='User')

    def __str__(self):
        return self.user.username