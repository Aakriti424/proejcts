from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib import messages
import django_filters

from .form import *
from .models import *
from templates import *

####✅✅✅Register###

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

    
####✅✅✅Login ####

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



####✅✅✅Application form ###

def JobseekerView(request, pk):
    if request.user.is_authenticated:
        form=JobSeekerForm()
        data={'form':form}
        if request.user.is_authenticated:
            if request.method=="POST":
                input=JobSeekerForm(request.POST, request.FILES)
                if input.is_valid():
                    job=Employer.objects.get(id=pk)
                    instance=input.save(commit=False)
                    instance.job=job
                    instance.user=request.user
                    instance.save()
                    return redirect('JobseekerProfile')
                return render(request, 'jobseeker.html', context={'form':form, 'error':'please fill all the field'})

        return render(request, 'jobseeker.html', context=data)
    else:
        return redirect('Login')


####✅✅✅Jobseeker dashboard ####

def JobseekerProfile(request):
    if request.user.is_authenticated:
        form_data=Employer.objects.all()
        return render(request, 'jobseekerprofile.html', context={'form':form_data})
    return redirect('Login')



####✅✅✅Vacancy form ####

def EmployerView(request):
    if request.user.is_authenticated:
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



####✅✅✅ Employer Dashboard ####

def EmployerProfileView(request):
    if request.user.is_authenticated:
        form_data=Employer.objects.all()
        user=request.user
        application_count=JobSeeker.objects.filter(job__user=user).count()
        accepted_count=JobSeeker.objects.filter(job__user=user,action='accept').count()
        return render(request, 'employerprofile.html', context={'form':form_data,'read':application_count, 'accepted':accepted_count})
    else:
        return redirect('Login')
    


### ✅✅✅ View all the vacancy created ###

def VacancyView(request):
    user=request.user
    filter=Employer.objects.filter(user=user)
    return render(request, 'vacancy.html', context={'form':filter})



####✅✅✅ View all the application created ####

def ApplicationView(request):
    if request.user.role=='employer':
        form=JobSeeker.objects.filter(job__user=request.user)
        return render(request, 'application.html', context={'form':form})
    else:
        form=JobSeeker.objects.filter(user=request.user)
        return render(request, 'appliedbyjobseeker.html', context={'form':form})




### ✅✅✅ Accept the applicant by employer ###

def accept(request, pk):
    form=JobSeeker.objects.get(id=pk)
    form.action=choices.Accept
    form.save()
    return redirect('EmployerProfile')




### ✅✅✅ View accepted resume in the jobseeker dashboard ####

def jobseekeraccept(request):
    if request.user.is_authenticated:
        if request.user.role=='job-seeker':
            form=JobSeeker.objects.filter(user=request.user, action=choices.Accept)
            return render(request, 'accept.html', context={'form':form})
        else:
            form=JobSeeker.objects.filter(job__user=request.user, action=choices.Accept)
            return render(request, 'accept.html', context={'form':form})
    return redirect('Login')




### ✅✅✅ View rejected resume in the jobseeker dashboard ####

def jobseekerreject(request):
    if request.user=='job-seeker':
        form=JobSeeker.objects.filter(user=request.user, action='reject')
        return render(request, 'reject.html', context={'form':form})
    else:
        form=JobSeeker.objects.filter(job__user=request.user, action='reject')
        return render(request, 'reject.html', context={'form':form})
    

###✅✅✅ Edit and delete option for employer ###

def edit(request, pk):
    if request.user.is_authenticated:
        pk_data=Employer.objects.get(id=pk)
        if request.method=="POST":
            form=EmployerForm(request.POST,request.FILES, pk_data)
            if form.is_valid():
                employer = form.save(commit=False)  
                employer.user = request.user      
                employer.save()                     
                return redirect('EmployerProfile')
        edit_data=EmployerForm(instance=pk_data)
        data={'form':edit_data}
        return render(request, 'employer.html', context={'form': form, 'error': 'Please fill the necessary data'})
    return redirect('Login')


def delete(request,pk):
    form=Employer.objects.get(id=pk)
    form.delete()
    return redirect('EmployerProfile')