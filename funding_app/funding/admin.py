from django.contrib import admin
from .models import FundingEvent, Categorization, Profile, Application
from unfold.admin import ModelAdmin

@admin.register(Categorization)
class CategorizationAdmin(ModelAdmin):
    icon = "tag"
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    list_display = ("project_type", "industry_fields", "event")
    search_fields = ("project_type", "eligibility_criteria")
    list_filter = ("industry_fields",)

    fieldsets = (
        ("Project Info", {
            "fields": ("project_type", "industry_fields", "event")
        }),
        ("Eligibility & Benefits", {
            "fields": ("eligibility_criteria", "benefits")
        }),
    )

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    icon = "user"
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    list_display = ("user", "organization", "role")
    search_fields = ("user__username", "organization")
    list_filter = ("role",)

    fieldsets = (
        ("User Information", {
            "fields": ("user", "organization", "role")
        }),
    )

@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    icon = "file"
    compressed_fields = True
    warn_unsaved_form = True
    change_form_show_cancel_button = True

    list_display = ("event", "applicant", "submitted_at", "status")
    search_fields = ("event__name", "applicant__username", "status")
    list_filter = ("status", "submitted_at")
    readonly_fields = ("submitted_at", "status")

    fieldsets = (
        ("Application Details", {
            "fields": ("event", "applicant", "status")
        }),
        ("Submission", {
            "fields": ("cover_letter", "attachment")
        }),
    )

@admin.register(FundingEvent)
class FundingEventAdmin(ModelAdmin):
    icon = "calendar"
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    list_filter_sheet = True
    change_form_show_cancel_button = True

    list_display = ("name", "country", "start_date", "end_date")
    search_fields = ("name", "country", "description")
    ordering = ("-start_date",)
    list_filter = ("country", "language")

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "url", "language", "country")
        }),
        ("Location & Host", {
            "fields": ("location", "host", "funder")
        }),
        ("Dates", {
            "fields": ("start_date", "end_date")
        }),
        ("Description", {
            "fields": ("description",)
        }),
    )