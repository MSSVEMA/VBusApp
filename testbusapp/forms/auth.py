from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.checks import messages
from django.views.generic import *
from django.urls import reverse_lazy
from django.shortcuts import *

from testbusapp.models import UserDetails


class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput())
    password = forms.CharField(label="password", widget=forms.PasswordInput())


class LoginView(View):
    def get(self,request):
        print(request.user)
        login_form=LoginForm()
        return render(request,template_name="login_form.html",context={'login_form':login_form})
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('testbusapp:search_buses_form')
        else:
            return render(request,template_name='invalid_login.html')

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput())
    age = forms.IntegerField(label="Age", widget=forms.NumberInput())
    gender=forms.ChoiceField(label="Gender",choices=[[1,'Male'],[2,'Female']])
    email = forms.EmailField(label="Email",widget=forms.EmailInput())
    mobile=forms.CharField(label="Mobile",widget=forms.TextInput())
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class SignUpView(View):

    def get(self,request):
        signup_form=SignUpForm()
        return render(request,template_name="signup_form.html",context={'signupform':signup_form})

    def post(self,request):
        # username = request.POST['username']
        # age = request.POST['age']
        # email = request.POST['email']
        # mobile = request.POST['mobile']
        # password = request.POST['password']

        signup_form=SignUpForm(request.POST)
        if signup_form.is_valid():
            gender=signup_form.cleaned_data['gender']
            if gender=='1':
                gender='Male'
            else:
                gender='Female'
            user_object=User.objects.create_user(username=signup_form.cleaned_data['username'],password=signup_form.cleaned_data['password'],email=signup_form.cleaned_data['email'])
            user_object.save()

            user_details_object=UserDetails(user=user_object,age=signup_form.cleaned_data['age'],mobile=signup_form.cleaned_data['mobile'],gender=gender)
            user_details_object.save()

            user=authenticate(request,username=signup_form.cleaned_data['username'],password=signup_form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                return redirect('/search_buses/')

from django.contrib.auth import logout

class HomeView(View):
    def get(self,request):
        # print(request.user)
        # if request.user.is_anonymous:
        #     return render(request, template_name="home.html")
        # else:
        #     return redirect('/search_buses/')
        return render(request, template_name="home.html")

def LogoutView(request):
    logout(request)
    return redirect('/home/')