from django.shortcuts import render ,redirect ,get_object_or_404
from .models import *
from .forms import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from .models import TimeRecord
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(username = username ,password = pass1)

        if user is not None:
            auth_login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect('/')
        else:
            messages.warning(request,"Wrong Credentials")
            return redirect('login')


    return render(request,'Main/login.html')

@login_required(login_url='/login')
def home (request):
    companies = company.objects.all()
    context = {'company':companies}
    return render(request, 'Main/home.html', context )

@login_required(login_url='/login')
def cpform(request):
    form = company_form()
    if request.method == 'POST':
        form = company_form(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
              

    context = {'form':form}
    return render(request, 'Main/cpform.html', context)

# def coform(request):
#     form = contact_form()
#     if request.method == 'POST':
#         form = contact_form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(request.META.get('HTTP_REFERER', 'home'))
#     context = {'form':form}
#     return render(request, 'Main/coform.html', context)

# views.py
@login_required(login_url='/login')
def coform(request, company_id=None):
    company_instance = get_object_or_404(company, pk=company_id) if company_id else None
    form = contact_form(initial={'company': company_instance}) if company_instance else contact_form()
    
    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    context = {'form': form}
    return render(request, 'Main/coform.html', context)



@login_required(login_url='/login')
def contact(request,pk):
    company_instance = get_object_or_404(company, pk=pk)

    # Then, filter contact_info objects by the company
    contacts = contact_info.objects.filter(company=company_instance)

    context = {'contacts':contacts, 'company_id':pk}
    return render (request, 'Main/contact.html', context)

@login_required(login_url='/login')
def company_delete(request,pk):
    companies= company.objects.get(id=pk)
    if request.method == 'POST':
        companies.delete()
        return redirect('home')
    
    return render (request, 'Main/delete.html')

@login_required(login_url='/login')
def coform_update(request,pk):
    contact = contact_info.objects.get(id = pk)
    form = contact_form(instance=contact)
    if request.method == 'POST':
        form = contact_form(request.POST,instance = contact)
        if form.is_valid():
            saved_contact = form.save()
            # Assuming you want to redirect to the 'contact' view for the company of this contact
            return redirect('contact', pk=saved_contact.company.id)
    return render (request, 'Main/coform.html',{'form':form})


@login_required(login_url='/login')
def cpform_update(request,pk):
    companys = company.objects.get(id = pk)
    form = company_form(instance=companys)
    if request.method == 'POST':
        form = company_form(request.POST,instance = companys)
        if form.is_valid():
            form.save()
            # Assuming you want to redirect to the 'contact' view for the company of this contact
            return redirect('home')
    return render (request, 'Main/cpform.html',{'form':form})

@csrf_exempt
@login_required(login_url='/login')
def save_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        startTime = parse_datetime(data.get('startTime'))
        stopTime = parse_datetime(data.get('stopTime'))

        # Check if startTime or stopTime is None
        if not startTime or not stopTime:
            return JsonResponse({"status": "error", "message": "Invalid start time or stop time"}, status=400)

        # Create a new TimeRecord instance and save it to the database
        time_record = TimeRecord(start_time=startTime, stop_time=stopTime)
        try:
            time_record.save()
            return JsonResponse({"status": "success", "message": "Time saved successfully"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are accepted"}, status=400)
