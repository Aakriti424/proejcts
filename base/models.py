from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=[
        ('employer', 'Employer'),
        ('job-seeker', 'JobSeeker'),
        ('admin', 'Admin')
    ]

    username=models.CharField(max_length=300, unique=True)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=50, choices=ROLE_CHOICES)
    address=models.CharField(max_length=300)
    contact=models.CharField(max_length=300)
    created_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.username
    

class Employer(models.Model):
    CONDTION_CHOICES=[
        ('accepted','Accepted'),
        ('rejected', 'Rejected')
    ]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    company=models.CharField(max_length=400)
    company_logo=models.ImageField(upload_to='company_logo/')
    post=models.CharField(max_length=50)
    requirement=models.TextField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    remains_till=models.DateField()
    website=models.URLField(null=True,blank=True)
    
    def __str__(self):
        return f"{self.company} as employer"
    

    
class JobSeeker(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    resume=models.ImageField(upload_to='resume/')
    job=models.ForeignKey(Employer, on_delete=models.CASCADE)
    bio=models.TextField()

    def __str__(self):
        return f"{self.user} as jobseeker"

