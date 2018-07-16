from django.forms import forms
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import DetailView

from testbusapp.models import *

class ShowBusesView(DetailView):

    template_name = "show_buses.html"

