from dateutil.relativedelta import relativedelta
from django import forms
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from datetime import datetime, date, timezone, timedelta

from testbusapp.models import *

from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

class AboutView(View):
    def get(self,request):
        return render(request,template_name="about.html")

class CancellationPolicyView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        return render(request,template_name="cancellation_policy.html")

class UserProfile(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        user_object=request.user

        context=dict()
        context['username']=user_object.username
        context['password']=user_object.password
        context['email']=user_object.email

        user_details_object=UserDetails.objects.get(user=user_object)

        context['age']=user_details_object.age
        context['gender']=user_details_object.gender
        context['mobile']=user_details_object.mobile
        return render(request,template_name="user_profile.html",context=context)

class EditUserProfile(LoginRequiredMixin,View):
    login_url = "/login"
    redirect_field_name = "redirected-to"

    def get(self,request):
        user_object=request.user

        context=dict()
        context['username']=user_object.username
        context['password']=user_object.password
        context['email']=user_object.email

        user_details_object=UserDetails.objects.get(user=user_object)

        context['age']=user_details_object.age
        context['gender']=user_details_object.gender
        context['mobile']=user_details_object.mobile
        return render(request,template_name="edit_profile.html",context=context)

    def post(self,request):
        updated_user_profile=request.POST['updated_user_profile']
        #print(updated_user_profile)
        updated_user_profile=updated_user_profile.split(';')
        username=updated_user_profile[0]
        age = int(updated_user_profile[1])
        gender = updated_user_profile[2]
        mobile = updated_user_profile[3]
        email = updated_user_profile[4]

        user_object=request.user
        user_object.username=username
        user_object.email=email
        user_object.save()

        user_details_object = UserDetails.objects.get(user=user_object)
        user_details_object.age=age
        user_details_object.mobile=mobile
        user_details_object.gender=gender
        user_details_object.save()

        return render(request,template_name="edit_user_profile_success.html")

class TermsView(View):
    def get(self,request):
        return render(request,template_name="terms.html")


class CitiesView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        cities_query_set=City.objects.values('name').all()
        return render(request,"cities.html",context={'cities':cities_query_set})

class DateForm(forms.Form):
    # requested_source_city=forms.CharField(label="From",widget=forms.TextInput())
    # requested_destination_city=forms.CharField(label="To",widget=forms.TextInput())
    date_of_journey=forms.DateField(label="Date of Journey",widget=forms.SelectDateWidget(),initial=date.today())


import calendar
class SearchBusesView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        city_names_object=City.objects.values('name')

        city_names=[]
        for city_name_dict in city_names_object:
            city_names.append(city_name_dict['name'])

        date_of_journey=DateForm()

        return render(request,template_name="search_buses_form.html",context={'city_names':city_names,'date_of_journey':date_of_journey})

    def post(self,request):
        requested_source_city=request.POST['requested_source_city']
        requested_destination_city=request.POST['requested_destination_city']
        date_of_journey_month=request.POST['date_of_journey_month']
        date_of_journey_day = request.POST['date_of_journey_day']
        date_of_journey_year = request.POST['date_of_journey_year']

        #print(request.user)
        #print(date_of_journey_day,date_of_journey_month,date_of_journey_year)

        try:
            date_of_journey_object=date(int(date_of_journey_year),int(date_of_journey_month),int(date_of_journey_day))
        except:
            return render(request, template_name="date_of_journey_wrong.html")

        today_date_object=date.today()
        max_date_of_journey_object=date.today()+relativedelta(months=+6)

        if (today_date_object<=date_of_journey_object<=max_date_of_journey_object)==False:
            return render(request,template_name="date_of_journey_wrong.html")

        date_of_journey_str=calendar.month_name[int(date_of_journey_month)]+" "+str(date_of_journey_day)+" "+str(date_of_journey_year)

        source_city_object=City.objects.get(name=requested_source_city)
        destination_city_object=City.objects.get(name=requested_destination_city)


        buses_query_set=BusAndCity.objects.all().filter(start_city=source_city_object).filter(city=destination_city_object).values("bus_id")

        list_of_dicts=[]

        for i in buses_query_set:
            bus_id=i['bus_id']

            src_time_query_set=BusAndCity.objects.filter(bus_id=bus_id).filter(city=source_city_object).values('time')
            dest_time_query_set = BusAndCity.objects.filter(bus_id=bus_id).filter(city=destination_city_object).values('time')

            source_arrival_time=src_time_query_set[0]['time']
            destination_reach_time = dest_time_query_set[0]['time']

            if today_date_object==date_of_journey_object:
                present_time=datetime.now()+timedelta(minutes=40)
                present_time=present_time.time()
                if present_time<source_arrival_time:

                    temp_dict=dict()

                    bus_object=Bus.objects.get(pk=bus_id)


                    booked_seats_count = len(SeatBookingDates.objects.filter(bus_id=bus_id).filter(seat_booked_date=date_of_journey_object).values())
                    seats_available=bus_object.total_seats-booked_seats_count

                    temp_dict['source_city']=source_city_object
                    temp_dict['source_arrival_time']=source_arrival_time
                    temp_dict['bus_object']=bus_object
                    temp_dict['seats_available']=seats_available


                    temp_dict['destination_city']=destination_city_object
                    temp_dict['destination_reach_time']=destination_reach_time


                    list_of_dicts.append(temp_dict)
            else:
                temp_dict = dict()

                bus_object = Bus.objects.get(pk=bus_id)

                booked_seats_count = len(SeatBookingDates.objects.filter(bus_id=bus_id).filter(
                    seat_booked_date=date_of_journey_object).values())
                seats_available = bus_object.total_seats - booked_seats_count

                temp_dict['source_city'] = source_city_object
                temp_dict['source_arrival_time'] = source_arrival_time
                temp_dict['bus_object'] = bus_object
                temp_dict['seats_available'] = seats_available

                temp_dict['destination_city'] = destination_city_object
                temp_dict['destination_reach_time'] = destination_reach_time

                list_of_dicts.append(temp_dict)

        context={
            'bus_cities_times_seats_details':list_of_dicts,
            'date_of_journey_dict': {'year':date_of_journey_year,'month':date_of_journey_month,'day':date_of_journey_day},
            'date_of_journey_str':date_of_journey_str
        }
        if len(list_of_dicts)==0:
            return render(request,"buses_unavailable.html",context=context)
        else:
            return render(request,"show_buses.html",context=context)


class ShowSeatsView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request,*args,**kwargs):
        bus_object=Bus.objects.get(pk=kwargs.get('bus_id'))
        source_city_name=kwargs.get('src')
        destination_city_name=kwargs.get('dest')
        day=kwargs.get('day')
        month=kwargs.get('month')
        year=kwargs.get('year')

        date_of_journey_object = date(int(year), int(month), int(day))
        date_of_journey_str = calendar.month_name[month] + " " + str(day) + " " + str(year)

        booked_seats_count = len(SeatBookingDates.objects.filter(bus_id=bus_object.id).filter(seat_booked_date=date_of_journey_object).values())
        seats_available = bus_object.total_seats - booked_seats_count

        source_city_object=City.objects.get(name=source_city_name)
        destination_city_object=City.objects.get(name=destination_city_name)

        arrival_time=BusAndCity.objects.values('time').filter(bus=bus_object).filter(city=source_city_object)
        reach_time=BusAndCity.objects.values('time').filter(bus=bus_object).filter(city=destination_city_object)

        seats_filled_in_bus_on_date_of_journey=SeatBookingDates.objects.filter(bus_id=bus_object.id).filter(seat_booked_date=date_of_journey_object).values('seat')
        seats_filled = []
        if bus_object.total_seats!=seats_available:
            for seat in seats_filled_in_bus_on_date_of_journey:
                seat_object=Seat.objects.get(bus_id=bus_object.id,pk=seat['seat'])
                seats_filled.append(str(seat_object.seat_i)+str(seat_object.seat_j))

        seats_list=[]
        for i in range(1,10):
            temp=[]
            for j in range(1,5):
                temp.append(str(i)+str(j))
            seats_list.append(temp)

        context={
            'bus_object':bus_object,
            'seats_list':seats_list,
            'source_city_name':source_city_name,
            'destination_city_name':destination_city_name,
            'times':{'arrival_time':arrival_time[0]['time'],'reach_time':reach_time[0]['time']},
            'seats_available':seats_available,
            'seats_filled':seats_filled,
            'date_of_journey_dict': {'year': year, 'month': month,'day': day},
            'date_of_journey_str': date_of_journey_str
        }
        return render(request,template_name="show_seats_of_a_bus.html",context=context)

class SeatsPassengersDetailsView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self,request):

        selected_seats = request.POST['selected_seats_tag']
        price = request.POST['price_tag']
        bus_object = Bus.objects.get(pk=int(request.POST['bus_id']))
        source_city_name = request.POST['source_city_name']
        destination_city_name = request.POST['destination_city_name']
        arrival_time = request.POST['arrival_time']
        reach_time = request.POST['reach_time']
        month = request.POST['month']
        day = request.POST['day']
        year = request.POST['year']
        date_of_journey_str = request.POST['date_of_journey_str']

        selected_seats_list=selected_seats.split(',')
        context = {
            'booked_seats': selected_seats,
            'price': price,
            'bus_object': bus_object,
            'source_city_name': source_city_name,
            'destination_city_name': destination_city_name,
            'times': {'arrival_time': arrival_time, 'reach_time': reach_time},
            'date_of_journey_dict': {'year': year, 'month': month, 'day': day},
            'date_of_journey_str': date_of_journey_str,
            'booked_seats_list':selected_seats_list,
            'seats_count':[i for i in range(len(selected_seats_list))],
            'booked_seats_count':len(selected_seats_list)
        }
        return render(request, template_name='seats_passengers_details.html', context=context)

class PaymentView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self,request):

        selected_seats = request.POST['selected_seats_tag']

        passengers_details=[]
        passengers_count=len(selected_seats.split(','))
        #print(passengers_count)

        passengers_details_str=request.POST['passengers_details']
        #print(passengers_details_str)
        passengers_details=passengers_details_str.split(';')
        #print(passengers_details)
        passengers_list=[]
        for i in range(passengers_count):
            passenger=passengers_details[i].split(',')
            passengers_list.append([passenger[0],passenger[1],passenger[2]])

        #print(passengers_list)

        price=request.POST['price_tag']
        bus_object=Bus.objects.get(pk=int(request.POST['bus_id']))
        source_city_name=request.POST['source_city_name']
        destination_city_name = request.POST['destination_city_name']
        arrival_time=request.POST['arrival_time']
        reach_time = request.POST['reach_time']
        month = request.POST['month']
        day = request.POST['day']
        year = request.POST['year']
        date_of_journey_str=request.POST['date_of_journey_str']

        context={
            'booked_seats':selected_seats,
            'price':price,
            'bus_object':bus_object,
            'source_city_name': source_city_name,
            'destination_city_name': destination_city_name,
            'times': {'arrival_time':arrival_time,'reach_time':reach_time},
            'date_of_journey_dict': {'year': year, 'month': month, 'day': day},
            'date_of_journey_str':date_of_journey_str,
            'passengers_details':passengers_list,
            'passengers_details_str':passengers_details_str
        }
        return render(request,template_name='payment_of_seats.html',context=context)



from django.core.mail import send_mail
def send_mail_test(booking_details,request):
    string=html_string(booking_details)
    send_mail(subject='Bus Seats Booking Mail',message="",from_email="vbusthewebsite@gmail.com",recipient_list=[request.user.email],html_message=string)

def html_string(booking_details):
    html_str="<html>" \
        "<body>" \
        "<center>" \
        "<div style='width:800px;background:#F9EECF;border:1px solid black;text-align:center'>" \
        "<h1>" \
        "<label style='color:blue;'>Booking Confirmed</label><br>" \
        "Booked Time : <u>"+booking_details['time_stamp']+"</u><br>" \
        "Ticket Number : <u>"+booking_details['ticket_id']+"</u><br>" \
        "Date of Journey: <u>"+booking_details['date_of_journey_str']+"</u><br>" \
        "Bus Id : "+str(booking_details['bus_object'].id)+"<br>" \
        "Bus Company : "+booking_details['bus_object'].company+"<br>" \
        "Bus Type : "+booking_details['bus_object'].bus_type+"<br>" \
        "User : "+booking_details['username']+"<br>" \
        "Booked Seats : <u>"+booking_details['booked_seats']+"</u><br>" \
        "Passengers : <u>"+booking_details['passengers_details_str']+"</u><br>" \
        "Price : "+booking_details['price']+"<br>" \
        "From : <u>"+booking_details['source_city_name']+"</u><br>" \
        "To : <u>"+booking_details['destination_city_name']+"</u><br>" \
        "Departure Time : <u>"+booking_details['arrival_time']+"</u><br>" \
        "Reach Time : <u>"+booking_details['reach_time']+"</u><br>" \
        "</h1>" \
        "</div>" \
        "</center>" \
        "</body>" \
        "</html>"
    return html_str

class PaymentConfirmedView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self,request):
        selected_seats=request.POST['selected_seats_tag']
        price=request.POST['price_tag']
        bus_object=Bus.objects.get(pk=int(request.POST['bus_id']))
        source_city_name=request.POST['source_city_name']
        destination_city_name = request.POST['destination_city_name']
        arrival_time=request.POST['arrival_time']
        reach_time = request.POST['reach_time']
        month = request.POST['month']
        day = request.POST['day']
        year = request.POST['year']
        date_of_journey_str = request.POST['date_of_journey_str']
        passengers_details_str = request.POST['passengers_details_str']
        #print(passengers_details_str)
        passengers_details = passengers_details_str.split(';')
        #print(passengers_details)
        passengers_list = []
        for i in range(len(passengers_details)-1):
            passenger = passengers_details[i].split(',')
            passengers_list.append([passenger[0], passenger[1], passenger[2]])

        #print(passengers_list)
        #print(passengers_details)

        passengers_details=passengers_list

        booking_time_stamp=datetime.now()
        date_of_journey_object = date(int(year), int(month), int(day))

        seats=selected_seats.split(",")
        i=0
        for seat in seats:
            seat_i=seat[0]
            seat_j=seat[1]

            seat_object = Seat.objects.get(bus=bus_object, seat_i=seat_i,seat_j=seat_j)

            user_object=request.user
            seat_booking_object=SeatBooking(bus=bus_object,seat=seat_object,seat_i=seat_i,seat_j=seat_j,user=user_object,source_city=source_city_name,destination_city=destination_city_name,price=price,time_stamp=booking_time_stamp)
            seat_booking_object.save()

            passenger_name=passengers_details[i][0]
            passenger_age=int(passengers_details[i][1])
            passenger_gender=passengers_details[i][2]
            seat_booked_dates_object=SeatBookingDates(bus=bus_object,seat=seat_object,seat_booked_date=date_of_journey_object,passenger_name=passenger_name,passenger_age=passenger_age,passenger_gender=passenger_gender)
            seat_booked_dates_object.save()
            i+=1

        ticket_id_and_seats_object=TicketIdAndSeats(bus=bus_object,seats_booked="".join(selected_seats),user=user_object,seats_booked_date=date_of_journey_object,source_city=source_city_name,destination_city=destination_city_name,price=price,time_stamp=booking_time_stamp)
        ticket_id_and_seats_object.save()

        context={
            'booked_seats':selected_seats,
            'price':price,
            'bus_object':bus_object,
            'source_city_name': source_city_name,
            'destination_city_name': destination_city_name,
            'times': {'arrival_time':arrival_time,'reach_time':reach_time},
            'ticket_id':ticket_id_and_seats_object.id,
            'date_of_journey_dict': {'year':year,'month':month,'day':day},
            'date_of_journey_str': date_of_journey_str,
            'time_stamp':booking_time_stamp,
            'passengers_details':passengers_details
        }

        booking_details={
            'booked_seats':str(selected_seats),
            'price':str(price),
            'bus_object':bus_object,
            'source_city_name': source_city_name,
            'destination_city_name': destination_city_name,
            'arrival_time':str(arrival_time),
            'reach_time':str(reach_time),
            'ticket_id':str(ticket_id_and_seats_object.id),
            'username':str(request.user),
            'date_of_journey_str': date_of_journey_str,
            'time_stamp': "{:%d %B %Y , %H:%M %p}".format(booking_time_stamp),
            'passengers_details_str':passengers_details_str
        }

        #send_ticket_to_user(context)
        try:
            send_mail_test(booking_details,request)
        except:
            #print("Unable to send email")
            pass
        return render(request,template_name='payment_confirmed.html',context=context)

class UserBookingsView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def get(self,request):
        user_object=request.user

        ticket_id_and_seats_query_set=TicketIdAndSeats.objects.filter(user=user_object).order_by("-seats_booked_date")

        if len(ticket_id_and_seats_query_set)==0:
            return render(request,template_name="no_bookings_yet.html")

        bookings_list = []
        for booking_object in ticket_id_and_seats_query_set:
            details_dict = dict()

            bus_object = Bus.objects.get(pk=booking_object.bus_id)
            details_dict['bus_id'] = bus_object.id
            details_dict['bus_company'] = bus_object.company
            details_dict['bus_type'] = bus_object.bus_type

            booking_time_stamp = booking_object.time_stamp
            details_dict['time_stamp'] = "{:%d %B %Y , %H:%M %p}".format(booking_time_stamp)

            details_dict['source_city']=booking_object.source_city
            details_dict['destination_city'] = booking_object.destination_city

            source_time=BusAndCity.objects.filter(bus=bus_object).filter(city=City.objects.get(name=booking_object.source_city)).values('time')
            destination_time = BusAndCity.objects.filter(bus=bus_object).filter(city=City.objects.get(name=booking_object.destination_city)).values('time')
            details_dict['source_time']=source_time[0]['time']
            details_dict['destination_time']=destination_time[0]['time']

            details_dict['date_of_journey']=booking_object.seats_booked_date
            details_dict['price'] = booking_object.price
            details_dict['seats_booked'] = booking_object.seats_booked

            present_date_object=datetime.now()
            present_time_object=present_date_object.time()

            date_of_journey_object=booking_object.seats_booked_date
            # date_of_journey_object=str(date_of_journey_object).split('-')
            # print(date_of_journey_object)
            # date_of_journey_object = date(int(date_of_journey_object[0]), int(date_of_journey_object[1]),int(date_of_journey_object[2]))
            # print(date_of_journey_object)


            if date.today()<=date_of_journey_object:
                #print(date.today(),date_of_journey_object)
                next_date_object=present_date_object+timedelta(hours=1)
                #print(next_date_object,date_of_journey_object)
                if next_date_object.date()<date_of_journey_object:
                    #print("11")
                    details_dict['cancel']=1
                elif next_date_object.date()==date_of_journey_object:
                    #print(next_date_object.date(), date_of_journey_object)
                    #print(next_date_object.time(), source_time[0]['time'])
                    if next_date_object.time()<=source_time[0]['time']:
                        #print("1")
                        details_dict['cancel']=1
                    else:
                        #print("2")
                        details_dict['cancel']=0
                else:
                    #print("3")
                    details_dict['cancel']=0
            else:
                #print("4")
                details_dict['cancel']=0

            details_dict['ticket_id']=booking_object.id
            bookings_list.append(details_dict)

        return render(request,template_name="user_bookings.html",context={'booking_details':bookings_list})

class CancelTicketsView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self,request):
        ticket_id=int(request.POST['ticket_id'])

        ticket_object=TicketIdAndSeats.objects.get(pk=ticket_id)
        bus_id=ticket_object.bus_id
        booked_seats_str=ticket_object.seats_booked
        date_of_journey_object=ticket_object.seats_booked_date

        booked_seats_list=booked_seats_str.split(',')

        booking_passengers_list=[]
        #booking_passengers_str=""
        for seat in booked_seats_list:

            temp_dict=dict()

            seat_i=int(seat[0])
            seat_j=int(seat[1])

            seat_object=Seat.objects.get(bus_id=bus_id,seat_i=seat_i,seat_j=seat_j)

            seat_booking_dates_object=SeatBookingDates.objects.get(bus_id=bus_id,seat_id=seat_object.id,seat_booked_date=date_of_journey_object)

            temp_dict['seat']=seat
            temp_dict['name']=seat_booking_dates_object.passenger_name
            temp_dict['age']=seat_booking_dates_object.passenger_age
            temp_dict['gender']=seat_booking_dates_object.passenger_gender
            booking_passengers_list.append(temp_dict)
            #booked_seats_str=booked_seats_str+str(seat)+","+str(seat_booking_dates_object.passenger_name)+","+str(seat_booking_dates_object.passenger_age)+","+str(seat_booking_dates_object.passenger_gender)+";"

        return render(request, template_name="cancel_tickets.html",context={'ticket_id': ticket_id, 'booked_passengers_list': booking_passengers_list})
        #return render(request,template_name="cancel_tickets.html",context={'ticket_id':ticket_id,'booked_passengers_list':booking_passengers_list,'booked_passengers_str':booked_seats_str})


def send_mail_cancel(cancel_details,request):
    string=html_string_cancel(cancel_details)
    send_mail(subject='Bus Seats Cancellation',message="",from_email="vbusthewebsite@gmail.com",recipient_list=[request.user.email],html_message=string)

def html_string_cancel(cancel_details):
    html_str="<html>" \
        "<body>" \
        "<center>" \
        "<div style='width:800px;background:#F9EECF;border:1px solid black;text-align:center'>" \
        "<h1>" \
        "<label style='color:red;'>Cancel Confirmed</label><br>" \
        "Booked Time : <u>"+cancel_details['time_stamp']+"</u><br>" \
        "Ticket Number : <u>"+cancel_details['ticket_id']+"</u><br>" \
        "Date of Journey: <u>"+cancel_details['date_of_journey_str']+"</u><br>" \
        "Bus Id : "+str(cancel_details['bus_object'].id)+"<br>" \
        "Bus Company : "+cancel_details['bus_object'].company+"<br>" \
        "Bus Type : "+cancel_details['bus_object'].bus_type+"<br>" \
        "User : "+cancel_details['username']+"<br>" \
        "Booked Seats : <u>"+cancel_details['booked_seats']+"</u><br>" \
        "Cancelled Seats : <u>"+cancel_details['cancelled_seats']+"</u><br>" \
        "From : <u>"+cancel_details['source_city_name']+"</u><br>" \
        "To : <u>"+cancel_details['destination_city_name']+"</u><br>" \
        "Departure Time : <u>"+cancel_details['arrival_time']+"</u><br>" \
        "Reach Time : <u>"+cancel_details['reach_time']+"</u><br>" \
        "</h1>" \
        "</div>" \
        "</center>" \
        "</body>" \
        "</html>"
    return html_str



class CancelTicketsConfirmedView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    def post(self,request):
        ticket_id=int(request.POST['ticket_id'])
        cancel_seats_str=request.POST['selected_seats_tag']
        cancel_seats_list=cancel_seats_str.split(',')

        cancel_details=dict()
        time_stamp=datetime.now()

        #print("cs",cancel_seats_str)
        ticket_object=TicketIdAndSeats.objects.get(pk=ticket_id)
        bus_id=ticket_object.bus_id
        booked_seats_str=ticket_object.seats_booked
        date_of_journey_object=ticket_object.seats_booked_date
        bus_object=Bus.objects.get(pk=bus_id)
        source_city_name=ticket_object.source_city
        destination_city_name = ticket_object.destination_city

        src_object=BusAndCity.objects.get(bus_id=bus_id,city=City.objects.get(name=source_city_name))
        dest_object=BusAndCity.objects.get(bus_id=bus_id, city=City.objects.get(name=destination_city_name))

        arrival_time=src_object.time
        reach_time=dest_object.time
        cancel_details={
            'booked_seats':booked_seats_str,
            'bus_object':bus_object,
            'source_city_name': source_city_name,
            'destination_city_name': destination_city_name,
            'arrival_time':str(arrival_time),
            'reach_time':str(reach_time),
            'ticket_id':str(ticket_id),
            'username':str(request.user),
            'date_of_journey_str': str(ticket_object.seats_booked_date),
            'time_stamp': "{:%d %B %Y , %H:%M %p}".format(time_stamp),
            'cancelled_seats':cancel_seats_str

        }
        booked_seats_list=booked_seats_str.split(',')

        #print("b",booked_seats_list,"c",cancel_seats_list)

        for seat in cancel_seats_list:

            seat_i=int(seat[0])
            seat_j=int(seat[1])

            seat_object=Seat.objects.get(bus_id=bus_id,seat_i=seat_i,seat_j=seat_j)

            seat_booking_dates_object=SeatBookingDates.objects.get(bus_id=bus_id,seat_id=seat_object.id,seat_booked_date=date_of_journey_object)

            seat_booking_dates_object.delete()

        if len(booked_seats_str)==len(cancel_seats_str):
            ticket_object.delete()
        else:
            for i in range(len(booked_seats_list)):
                if booked_seats_list[i] in cancel_seats_list:
                    booked_seats_list[i]=0


            updated_booked_seats_str=""

            for i in range(len(booked_seats_list)):
                if booked_seats_list[i]!=0:
                    if updated_booked_seats_str=="":
                        updated_booked_seats_str=booked_seats_list[i]
                    else:
                        updated_booked_seats_str=updated_booked_seats_str+","+booked_seats_list[i]

            #print("u",updated_booked_seats_str)

            ticket_object.seats_booked=updated_booked_seats_str
            ticket_object.price=ticket_object.price-(100*len(cancel_seats_list))
            ticket_object.save()

        try:
            send_mail_cancel(cancel_details,request)
        except:
            #print("Unable to send email")
            pass
        return render(request,template_name="cancel_tickets_confirmed.html",context={'cancel_seats_str':cancel_seats_str})