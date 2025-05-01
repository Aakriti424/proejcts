from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
import django_filters
from .form import *
from .models import *
from templates import *

# Create your views here.

class Register(generic.CreateView):
    model=User
    form_class=RegisterForm
    template_name='register.html'
    success_url=reverse_lazy('Login')
    
    def form_valid(self, form):
        data=form.save(commit=False)
        data.set_password(data.password)
        data.save()

        
        role=form.cleaned_data.get('role')
        if role:
            group,_=Group.objects.get_or_create(name=role)
            data.groups.add(group)
        return super().form_valid(form)

    


def Login(request):
    form=User.objects.all()
    data={'form':form}
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(email=email, password=password)
        if user==None:
            return render(request, 'login.html', context=({'form':form,'error':"Invalid username or password"}))
        auth_login(request, user)
        if request.user.role=='job-seeker':
            return redirect('JobseekerProfile')
        else:
            return redirect('EmployerProfile')
    return render(request, 'login.html', data)


def Homepage(request):
   return render(request, 'index.html')


def JobseekerView(request):
    form=JobSeekerForm()
    data={'form':form}
    if request.user.is_authenticated:
        if request.method=="POST":
            input=JobSeekerForm(request.POST, request.FILES)
            if input.is_valid():
                instance=input.save(commit=False)
                instance.user=request.user
                instance.save()
                return redirect('JobseekerProfile')
            return render(request, 'jobseeker.html', context={'form':form, 'error':'please fill all the field'})


        return render(request, 'jobseeker.html', context=data)
    else:
        return redirect('Login')

def JobseekerProfile(request):
    if request.user.is_authenticated:
        form_data=Employer.objects.all()
        data={'form':form_data}
        return render(request, 'jobseekerprofile.html', context=data)
    return redirect('Login')

def EmployerView(request):
    if request.method == "POST":
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.save(commit=False)  
            employer.user = request.user      
            employer.save()                     
            return redirect('EmployerProfile')
        else:
            return render(request, 'employer.html', context={'form': form, 'error': 'Please fill the necessary data'})
    return render(request, 'employer.html', context={'form': EmployerForm()})



def EmployerProfileView(request):
    if request.user.is_authenticated:
        form_data=Employer.objects.all()
        application_count=JobSeeker.objects.filter(job__user=request.user).count()
        return render(request, 'employerprofile.html', context={'form':form_data, 'count':application_count})
    else:
        return render('Login')
    



def ApplicationView(request):
    user=request.user
    filter=Employer.objects.filter(user=user)
    return render(request, 'application.html', context={'form':filter})