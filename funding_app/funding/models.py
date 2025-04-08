from django.db import models
from django.contrib.auth.models import User

class FundingEvent(models.Model):
    # Adapted from the webscraping "Convocatoria" model
    name = models.CharField(max_length=255)  # nombre_de_la_convocatoria
    url = models.URLField()  # enlace_de_la_convocatoria
    language = models.CharField(max_length=50, blank=True, null=True)  # idioma
    country = models.CharField(max_length=100, blank=True, null=True)  # pais_que_convoca
    start_date = models.DateField(blank=True, null=True)  # fecha_de_apertura
    end_date = models.DateField(blank=True, null=True)  # fecha_de_cierre
    description = models.TextField(blank=True, null=True)  # For any additional info

    # Optional fields you may keep if needed
    location = models.CharField(max_length=255, blank=True, null=True)
    host = models.CharField(max_length=255, blank=True, null=True)
    funder = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Categorization(models.Model):
    # Fields mapped from the webscraping model "Convocatoria"
    project_type = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Type of project or proposal accepted (tipo_de_proyecto_o_propuesta_que_se_puede_presentar)"
    )
    eligibility_criteria = models.TextField(
        blank=True,
        null=True,
        help_text="Criteria for participation (quienes_pueden_participar)"
    )
    benefits = models.TextField(
        blank=True,
        null=True,
        help_text="Benefits or prizes offered (beneficios)"
    )
    # Optional: Include industry_fields if applicable
    industry_fields = models.CharField(max_length=255, blank=True, null=True)
    
    # Link to the FundingEvent (one-to-one)
    event = models.OneToOneField(FundingEvent, on_delete=models.CASCADE, related_name="categorization")

    def __str__(self):
        return f"{self.project_type} - {self.event.name}"

# Renaming the custom user extension to Profile to avoid conflict with Django's built-in User model
class Profile(models.Model):
    USER_ROLES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.PositiveIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='User')

    def __str__(self):
        return self.user.username

class Application(models.Model):
    # Model to allow users to apply for funding events.
    event = models.ForeignKey(FundingEvent, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    cover_letter = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Application by {self.applicant.username} for {self.event.name}"