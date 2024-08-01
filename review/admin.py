from django.contrib import admin
from review.models import *
# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')

admin.site.register(Ticket, TicketAdmin)