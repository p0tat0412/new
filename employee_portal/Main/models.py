from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class company(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank= True)
    name = models.CharField(max_length = 100)
    keyid = models.CharField(max_length = 100)
    catagory = models.CharField(max_length= 100)
    description = models.TextField(null = True, blank = True)
    company_description = models.CharField(max_length = 100)
    website_link = models.CharField(max_length = 100)
    email = models.EmailField(null = True)

    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
class contact_info(models.Model):
    company = models.ForeignKey(company, on_delete=models.SET_NULL, null = True, blank = True)
    individuals_name = models.CharField(max_length = 100)
    position = models.CharField(max_length = 100)
    linked_in = models.CharField(max_length = 100)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 20)
    so_phone_number = models.CharField(max_length = 100)
    so_information = models.CharField(max_length = 100, null = True, blank = True)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        company_name = self.company.name if self.company else "No Company"
        return f'{company_name}-{self.individuals_name}'
    

class TimeRecord(models.Model):
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    def __str__(self):
        return f'{self.start_time}<<<<<<<<<<<<<>>>>>>>>>>>>>>>{self.stop_time}'