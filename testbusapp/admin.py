from django.contrib import admin


# Register your models here.
from testbusapp.models import Bus,City,BusAndCity,Seat

admin.site.register(City)
admin.site.register(Bus)
admin.site.register(BusAndCity)
admin.site.register(Seat)

