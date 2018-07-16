from django.urls import path


from testbusapp.views import *
from testbusapp.forms import *
from django.conf import settings
from django.conf.urls import include,url
#from rest_framework_jwt.views import *

app_name = "testbusapp"

urlpatterns = [

    path('home/',HomeView.as_view(),name="home"),
    path('login/',LoginView.as_view(),name="login"),
    path('signup/',SignUpView.as_view(),name="signup"),
    path('logout/',LogoutView,name="logout"),
    path('about/',AboutView.as_view(),name="about"),
    path('terms/',TermsView.as_view(),name="terms"),
    path('cities/',CitiesView.as_view(),name="cities"),
    path('user_bookings/',UserBookingsView.as_view(),name="user_bookings"),
    path('user_profile/',UserProfile.as_view(),name="user_profile"),
    path('edit_profile/',EditUserProfile.as_view(),name="edit_profile"),
    path('cancel_tickets/',CancelTicketsView.as_view(),name="cancel_tickets"),
    path('cancel_tickets_confirm/',CancelTicketsConfirmedView.as_view(),name="cancel_tickets_confirm"),
    path('search_buses/',SearchBusesView.as_view(),name="search_buses_form"),
    path('search_buses/show_buses/',ShowBusesView.as_view(),name="show_buses"),
    path('search_buses/show_seats/<int:bus_id>/<str:src>/<str:dest>/<int:day>/<int:month>/<int:year>/',ShowSeatsView.as_view(),name="show_seats_of_a_bus"),
    path('seats_passengers_details/',SeatsPassengersDetailsView.as_view(),name="seats_passengers_details"),
    path('payment/',PaymentView.as_view(),name="payment"),
    path('payment_confirmed/',PaymentConfirmedView.as_view(),name="payment_confirmed"),
    path('cancellation_policy/',CancellationPolicyView.as_view(),name="cancellation_policy")
#     path('logout/',Logout_view,name="logout"),
#     path('colleges/',CollegeView.as_view(),name="college_details"),
#     path('colleges/<int:pk>/',CollegeDetailsView.as_view(),name="particular_college_details"),
#     path('colleges/addcollege/',CreateCollegeView.as_view(),name="add_college"),
#     path('colleges/<int:pk>/addstudent',AddStudentView.as_view(),name="add_student"),
#     path('colleges/<int:pk>/editcollege',EditCollegeView.as_view(),name="edit_college"),
#     path('colleges/<int:college_id>/<int:pk>/editstudent',EditStudentView.as_view(),name="edit_student"),
#     path('colleges/<int:pk>/deletecollege/',DeleteCollegeView.as_view(),name="delete_college"),
#     path('colleges/<int:college_id>/<int:pk>/deletestudent',DeleteStudentView.as_view(),name="delete_student"),
#     path('departments/',DepartmentsView.as_view(),name="college_details"),
#     # path('api/colleges_list/',colleges_list,name='college_list_json'),
#      path('api/college_details/<int:pk>/',college_details,name='college_details_json'),
#     # path('api/colleges_list/<int:pk>/students/',college_students.as_view(),name='college_students_json'),
#
# #    path('colleges_/', collegeListViewSerializer.as_view(), name="colleges_"),
#     path('colleges_/add/', CreateCollegeViewSerializer.as_view(), name="addCollege_"),
#     path('colleges_/<int:pk>/edit/', EditCollegeViewSerializer.as_view(), name="editCollege_"),
#     path('colleges_/<int:pk>/delete/', DeleteCollegeViewSerializer.as_view(), name='deleteCollege_'),
#
#     #path('colleges_/<int:pk>/', CollegeDetailsViewSerializer.as_view(), name='collegesmarks_'),
#     path('colleges_/<int:cpk>/students/<int:pk>/', StudentDetailViewSerializer.as_view(), name='studentDetails_'),
#     path('colleges_/<int:pk>/students/addstudent/', CreateStudenteViewSerializer.as_view(), name="addStudent_"),
#     path('colleges_/<int:cpk>/students/<int:pk>/editstudent/', EditStudentViewSerializer.as_view(),
#          name="editStudent_"),
#     path('colleges_/<int:cpk>/students/<int:pk>/deletestudent/', DeleteStudentViewSerializer.as_view(),
#          name="deleteStudent_"),
#
#     path('api/api-auth-token/',obtain_jwt_token)
]
