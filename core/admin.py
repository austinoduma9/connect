
# Register your models here.
from django.contrib import admin
from .models import CustomUser, Connection, Idea, InvestorInterest, Event  # Import your models

# Register your models
admin.site.register(CustomUser)
admin.site.register(Connection)
admin.site.register(Idea)
admin.site.register(InvestorInterest)
admin.site.register(Event)