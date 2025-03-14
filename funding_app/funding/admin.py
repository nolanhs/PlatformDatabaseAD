from django.contrib import admin
from .models import FundingEvent, Categorization, User

admin.site.register(FundingEvent)
admin.site.register(Categorization)
admin.site.register(User)