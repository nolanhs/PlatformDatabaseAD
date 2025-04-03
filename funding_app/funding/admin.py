from django.contrib import admin
from .models import FundingEvent, Categorization, User, Application
from unfold.admin import ModelAdmin

admin.site.register(Categorization)
admin.site.register(User)
admin.site.register(Application)

@admin.register(FundingEvent)
class FundingEventAdmin(ModelAdmin):

    pass