from django.contrib import admin
from review.models import *
# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_created')

class userFollowsAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(UserFollows, userFollowsAdmin)