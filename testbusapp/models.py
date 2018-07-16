from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class UserDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    gender=models.CharField(max_length=10,default=None)
    mobile=models.CharField(max_length=100)


class City(models.Model):
    name=models.CharField(max_length=50)

class Bus(models.Model):
    company=models.CharField(max_length=20)
    bus_type=models.CharField(max_length=20)
    total_seats=models.IntegerField()
    rows=models.IntegerField()
    columns=models.IntegerField()
    start_city=models.ForeignKey(City,on_delete=models.CASCADE,related_name="start_city_s")
    end_city = models.ForeignKey(City,on_delete=models.CASCADE,related_name="end_city_s")
    # seats_available=models.IntegerField()

class BusAndCity(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.CASCADE,related_name="city")
    start_city=models.ForeignKey(City,on_delete=models.CASCADE,related_name="start_city")
    time=models.TimeField()

class Seat(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.CASCADE)
    seat_i=models.IntegerField()
    seat_j=models.IntegerField()
    # vacant=models.BooleanField()
    # seat_booked_date=models.DateField(null=True,blank=True)

class SeatBookingDates(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.DO_NOTHING)
    seat=models.ForeignKey(Seat,on_delete=models.DO_NOTHING)
    seat_booked_date=models.DateField()
    passenger_name=models.CharField(max_length=100,default=None)
    passenger_age=models.IntegerField(default=20)
    passenger_gender=models.CharField(max_length=10,default=None)

class SeatBooking(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.DO_NOTHING)
    seat=models.ForeignKey(Seat,on_delete=models.DO_NOTHING)
    seat_i=models.IntegerField()
    seat_j=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    seat_booked_date=models.DateField(null=True,blank=True)
    source_city=models.CharField(max_length=50)
    destination_city=models.CharField(max_length=50)
    price=models.IntegerField()
    time_stamp=models.DateTimeField()

class TicketIdAndSeats(models.Model):
    bus=models.ForeignKey(Bus,on_delete=models.DO_NOTHING)
    seats_booked=models.CharField(max_length=1000)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    seats_booked_date=models.DateField(null=True,blank=True)
    source_city=models.CharField(max_length=50)
    destination_city=models.CharField(max_length=50)
    price=models.IntegerField()
    time_stamp=models.DateTimeField()

# source_city=models.ForeignKey(City,on_delete=models.DO_NOTHING)
# destination_city=models.ForeignKey(City,on_delete=models.DO_NOTHING)

# class Bookings(models.Model):
