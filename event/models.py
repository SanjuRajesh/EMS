from django.db import models
from django.contrib.auth.models import User 



class Dept_Club(models.Model):
    dc_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.dc_name
    
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    designation = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dept_club = models.ForeignKey(Dept_Club, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 


    
class Duty_Alloc(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    dept_club = models.ForeignKey(Dept_Club, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dept_club} - {self.faculty}"

class Event(models.Model):
    mode_choices = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid')
    ]
    title = models.CharField(max_length=100)
    mode = models.CharField(max_length=10, choices=mode_choices)
    no_participants = models.IntegerField()
    description = models.TextField()
    from_date = models.DateField()
    from_time = models.TimeField()
    date_to = models.DateField()
    time_to = models.TimeField()
    dept_club = models.ForeignKey(Dept_Club, on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags', on_delete=models.DO_NOTHING)
    brochure = models.ImageField(upload_to='brochures/')

    def __str__(self):
        return self.title
    

class Permission(models.Model):
    status_choices = [
         ('APPROVED', 'Approved'),
         ('REJECTED', 'Rejected'),
         ('PENDING', 'Pending')
    ]
    status = models.CharField(max_length=10, choices=status_choices)
    Event = models.ForeignKey(Event, on_delete=models.CASCADE)  


class Tags(models.Model):
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag

class Event_Report(models.Model):
    date = models.DateField(auto_now_add=True)
    report = models.TextField(null=True)
    youtube_link = models.URLField(null=True,blank=True)
    photo = models.ImageField(upload_to='event_reports/photos/', null=True, blank=True)
    alternate_photo = models.ImageField(upload_to='event_reports/alternate_photos/', null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Report for {self.event.title} on {self.date}"

