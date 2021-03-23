from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from easy_pdf.rendering import render_to_pdf_response
from django.urls import reverse
import json
from django.shortcuts import redirect
from .models import *

# Create your views here.



def index(request):
    return render(request,'navecomClient/index.html')
