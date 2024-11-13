from tkinter.tix import Form
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Forms)
admin.site.register(TurfBooking)
admin.site.register(Events_Ticket)
admin.site.register(Event_Bookings)
admin.site.register(User)
