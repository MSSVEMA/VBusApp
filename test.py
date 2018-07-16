import os,sys,django

from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE',"testbusproject.settings")
django.setup()
from testbusapp.models import *

# visakhapatnam_city=City(name="visakhapatnam")
# visakhapatnam_city.save()
# razole_city=City(name="razole")
# razole_city.save()

# visakhapatnam_city=City.objects.get(pk=1)
# razole_city=City.objects.get(pk=2)

# bus=Bus(company="APSRTC",bus_type="SUPER_LUXURY",total_seats=36,rows=9,columns=4,start_city=visakhapatnam_city,end_city=razole_city)
# bus.save()
#
# bus_pk=Bus.objects.get(pk=1)
# city_pk=City.objects.get(name="visakhapatnam")
# bus_city=BusAndCity(time="21:30",bus=bus_pk,city=city_pk,start_city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=1)
# city_pk=City.objects.get(name="razole")
# bus_city=BusAndCity(time="5:00",bus=bus_pk,city=city_pk,start_city=)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=1)
# for i in range(1,10):
#     for j in range(1,5):
#         seat=Seat(seat_i=i,seat_j=j,vacant=True,bus=bus_pk)
#         seat.save()
#
# bus=Bus(company="APSRTC",bus_type="SUPER_LUXURY",total_seats=36,rows=9,columns=4,seats_available=36)
# bus.save()
#
# bus_pk=Bus.objects.get(pk=2)
# city_pk=City.objects.get(name="visakhapatnam")
# bus_city=BusAndCity(time="18:30",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=2)
# city_pk=City.objects.get(name="razole")
# bus_city=BusAndCity(time="2:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=2)
# for i in range(1,10):
#     for j in range(1,5):
#         seat=Seat(seat_i=i,seat_j=j,vacant=True,bus=bus_pk)
#         seat.save()
#
#
#
# bus=Bus(company="APSRTC",bus_type="SUPER_LUXURY",total_seats=36,rows=9,columns=4,seats_available=36)
# bus.save()
#
# bus_pk=Bus.objects.get(pk=3)
# city_pk=City.objects.get(name="visakhapatnam")
# bus_city=BusAndCity(time="20:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=3)
# city_pk=City.objects.get(name="razole")
# bus_city=BusAndCity(time="4:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=3)
# for i in range(1,10):
#     for j in range(1,5):
#         seat=Seat(seat_i=i,seat_j=j,vacant=True,bus=bus_pk)
#         seat.save()
#
# bus=Bus(company="APSRTC",bus_type="SUPER_LUXURY",total_seats=36,rows=9,columns=4,seats_available=36)
# bus.save()
#
# bus_pk=Bus.objects.get(pk=4)
# city_pk=City.objects.get(name="visakhapatnam")
# bus_city=BusAndCity(time="23:55",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=4)
# city_pk=City.objects.get(name="razole")
# bus_city=BusAndCity(time="7:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=4)
# for i in range(1,10):
#     for j in range(1,5):
#         seat=Seat(seat_i=i,seat_j=j,vacant=True,bus=bus_pk)
#         seat.save()
#
# city=City(name="hyderabad")
# city.save()
#
# bus=Bus(company="APSRTC",bus_type="SUPER_LUXURY",total_seats=36,rows=9,columns=4,seats_available=36)
# bus.save()
#
# bus_pk=Bus.objects.get(pk=5)
# city_pk=City.objects.get(name="visakhapatnam")
# bus_city=BusAndCity(time="8:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=5)
# city_pk=City.objects.get(name="hyderabad")
# bus_city=BusAndCity(time="22:00",bus=bus_pk,city=city_pk)
# bus_city.save()
#
# bus_pk=Bus.objects.get(pk=5)
# for i in range(1,10):
#     for j in range(1,5):
#         seat=Seat(seat_i=i,seat_j=j,vacant=True,bus=bus_pk)
#         seat.save()
#
# query_set1=BusAndCity.objects.values().filter(Q(city_id=City.objects.get(name='visakhapatnam'))&Q(city_id=City.objects.get(name="razole")))
# query_set2=BusAndCity.objects.all().filter(city='razole')
#
#
# print(query_set1)
# print(query_set2)
#
# print(query_set1[0]['bus_id'])
#
# requested_source_city='visakhapatnam'
# requested_destination_city='razole'
#
# src_object=City.objects.get(name=requested_source_city)
# dest_object=City.objects.get(name=requested_destination_city)
#
# buses_query_set = BusAndCity.objects.all().filter(Q(city=src_object) | Q(city=dest_object)).values()
#
# print(*buses_query_set,sep="\n")
#
# list_of_dicts=[]
# i=0
# for bus_query_set in buses_query_set:
#     if(i%2==0):
#         temp_dict=dict()
#         bus_object=Bus.objects.get(pk=bus_query_set['bus_id'])
#
#         source_city_name=City.objects.get(pk=bus_query_set['city_id'])
#         source_arrival_time=bus_query_set['time']
#
#         temp_dict['source_city']=source_city_name
#         temp_dict['source_arrival_time']=source_arrival_time
#         temp_dict['bus_object']=bus_object
#     else:
#         destination_city_name = City.objects.get(pk=bus_query_set['city_id'])
#         destination_reach_time = bus_query_set['time']
#
#         temp_dict['destination_city']=destination_city_name
#         temp_dict['destination_reach_time']=destination_reach_time
#
#         list_of_dicts.append(temp_dict)
#     i+=1
#
# context={
#     'bus_cities_times_seats_details':list_of_dicts
#     }
#
# print(context)
#
# pass






# {% for i in "x"|ljust:"3" %}
#     <!-- Do stuff -->
#     {{forloop.counter}}
# {% endfor %}


# bus_object=Bus.objects.get(pk=1)
# seat_object = Seat.objects.get(bus=bus_object, seat_i=1,seat_j=1)
# print(seat_object)

# from django.contrib.auth.models import User
#
# print(User.objects.get(username="Vema"))

# seats = Seat.objects.filter(bus_id=1).values('seat_i', 'seat_j', 'vacant')
#
# seats_vacant = []
# for seat in seats:
#     temp = []
#     if seat['vacant'] == False:
#         temp.append([seat['seat_i'],seat['seat_j']])
#         seats_vacant.append(temp)
#
# print(seats_v)

# bus_object=Bus.objects.get(pk=1)
# bus_object.seats_available=36
# bus_object.save()
#
# for i in range(1,33):
#     seat_object=Seat.objects.get(pk=i)
#     seat_object.vacant=True
#     seat_object.save()

# cities=City.objects.values('name')
# print(cities)

# query_set=SeatBookingDates.objects.filter(bus_id=1).values()
# print(len(query_set))

# from datetime import datetime,date
# date_obj=date.today()
# SeatBookingDates(bus=Bus.objects.get(pk=1),seat=Seat.objects.get(pk=1),seat_booked_date=date_obj).save()

# source_time=BusAndCity.objects.filter(bus_id=1).filter(city=City.objects.get(name="visakhapatnam")).values('time')
# print(source_time[0]['time'])
# b=source_time[0]['time']
# import datetime
#
# datetime.timedelta
# print(datetime.datetime.now().time())
# p=datetime.datetime.now()
# print(p)
# print(datetime.datetime.today())
# print(p.time()<b)
#
# n=p+datetime.timedelta(hours=3)
# print(n.time())
#
# datetime

# ticket_object=TicketIdAndSeats.objects.get(pk=10)
# ticket_object.seats_booked="21"
# ticket_object.save()

# for i in range(8,16):
#     Bus(company="APSRTC",bus_type="SUPER LUXURY",total_seats=36,rows=9,columns=4,start_city_id=2,end_city_id=1).save()

# for i in range(1,16):
#     for j in range(1,10):
#         for k in range(1,5):
#             Seat(seat_i=j,seat_j=k,bus_id=i).save()

# buses=BusAndCity.objects.all().filter(start_city_id=1).filter(city_id=2).values("bus_id")
# print(buses)

from datetime import datetime,date,timedelta

# p=datetime.now()
# print(p)
# t=p.time()
# print(t)
#
# bus_object=BusAndCity.objects.get(pk=1)
# print(bus_object.time)
#
# print(t<bus_object.time)

# p=datetime.now()
# print(p)
# n=p+timedelta(hours=3)
# print(n.time())
#
# bus_object=BusAndCity.objects.get(pk=13)
# print(bus_object.time)
#
# print(n.time()<bus_object.time)
#
# p=date.today()
# print(p,type(p).__name__)
#
# sb=TicketIdAndSeats.objects.get(pk=1)
# sb=sb.seats_booked_date
#
# print(sb,type(sb).__name__)
#
# print(p<sb)

# p=datetime.now()
# print(p)
# print(p.today())
# print(p.date())

city_q=City.objects.values('name').all()
print(city_q)