from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import UserCreationFormExtended
from django.utils import timezone
from .forms import *
from .models import *


# Create your views here.
def home(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(from_date__gt=now.date()) | Event.objects.filter(from_date=now.date(), from_time__gt=now.time())
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request,'events/home.html',context)

@login_required
def notification(request):
    return render(request,'events/notify.html')

def admin_check(user):
    return user.is_superuser 

@user_passes_test(admin_check)
def update_event_status(request, event_id, status):
    event = get_object_or_404(Event, id=event_id)
    permission, created = Permission.objects.get_or_create(Event=event)
    permission.status = status
    permission.save()
    return redirect('events')

@login_required
def events(request):
    if request.user.is_superuser:
        user_events = Event.objects.all()
    else:
        try:
            faculty = Faculty.objects.get(user=request.user)
            user_dept_club = faculty.dept_club
            user_events = Event.objects.filter(dept_club=user_dept_club)
        except Faculty.DoesNotExist:
            user_events = Event.objects.none()

    return render(request, 'events/events.html', {'events': user_events})

@login_required
def report_page(request):
    if request.user.is_superuser:
        reports = Event_Report.objects.all()
    else:
        try:
            faculty = Faculty.objects.get(user=request.user)
            user_dept_club = faculty.dept_club
            reports = Event_Report.objects.filter(event__dept_club=user_dept_club)
        except Faculty.DoesNotExist:
            reports = Event_Report.objects.none()

    context = {
        'reports': reports,
    }

    return render(request, 'events/report.html', context)


@login_required()
def add_event(request):
    current_user = request.user
    current_faculty = Faculty.objects.get(user=current_user)
    default_club_id = current_faculty.dept_club.id if current_faculty else None
    default_club_name = current_faculty.dept_club.dc_name if current_faculty else ""

    if request.method == 'POST':
        form = addeventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'events/conform.html')  # Ensure this path is correct
        else:
            print(form.errors)  # Print form errors to debug
    else:
        # Initialize the form with the dept_club field set to default value
        form = addeventForm(initial={'dept_club': default_club_id})

    return render(request, 'events/add_event.html', {'form': form, 'default_club_id': default_club_id, 'default_club_name': default_club_name})

from .models import Event  # Import the Event model if not already imported



def search_event(request):
    title_query = request.GET.get('title')
    department_query = request.GET.get('department_club')

    events = Event.objects.all()

    if title_query:
        # Perform case-insensitive search for title
        events = events.filter(title__icontains=title_query)

    if department_query:
        # Perform case-insensitive search for department/club
        events = events.filter(dept_club__dc_name__icontains=department_query)

    return render(request, 'events/search_event.html', {'events': events})



def search_report(request):
    query_name = request.GET.get('name', '')
    query_tag = request.GET.get('tag', '')
    department_query = request.GET.get('department_club', '')
    results = Event_Report.objects.all()

    if query_name:
        results = results.filter(event__title__icontains=query_name)
    if query_tag:
        results = results.filter(event__tag__tag__icontains=query_tag)
    if department_query:
        # Perform case-insensitive search for department/club
        results = results.filter(event__dept_club__dc_name__icontains=department_query)

    return render(request, 'events/search_report.html', {'reports': results})

@login_required
def add_report(request):
    if request.method == 'POST':
        form = EventReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_page')  # Redirect to the report page after saving
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = EventReportForm()

    return render(request, 'events/add_report.html', {'form': form})
 

@login_required()
@user_passes_test(admin_check)
def duty_alloc(request):
    return render(request,'events/duty_alloc.html')

@login_required
@user_passes_test(admin_check)
def allocated_duty(request):
    faculties = Faculty.objects.all()  # Fetch all Faculty objects
    dept_clubs = Dept_Club.objects.all()  # Fetch all Dept_Club objects
    duty_allocs = Duty_Alloc.objects.all()  # Fetch all Duty_Alloc objects

    context = {
        'faculties': faculties,
        'dept_clubs': dept_clubs,
        'duty_allocs': duty_allocs
    }
    return render(request, 'events/allocated_duty.html', context)

@login_required
@user_passes_test(admin_check)
def add_allocation(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty')
        dept_club_id = request.POST.get('dept_club')

        faculty = Faculty.objects.get(id=faculty_id)
        dept_club = Dept_Club.objects.get(id=dept_club_id)

        Duty_Alloc.objects.create(faculty=faculty, dept_club=dept_club)
        
    faculties = Faculty.objects.all()
    dept_clubs = Dept_Club.objects.all()
    duty_allocs = Duty_Alloc.objects.all()

    context = {
        'faculties': faculties,
        'dept_clubs': dept_clubs,
        'duty_allocs': duty_allocs
    }

    return render(request, 'events/add_allocation.html', context)

@login_required
@user_passes_test(admin_check)
def add_dept_club(request):
    if request.method == "POST":
        if "add_dept_club" in request.POST:
            # Handle the new department club form submission
            dept_club_name = request.POST.get("dept_club_name")
            if dept_club_name:
                Dept_Club.objects.create(dc_name=dept_club_name)
    return render(request, 'events/add_dept_club.html')


@login_required
@user_passes_test(admin_check)
def add_user(request):
    if not request.user.is_superuser:
        # Redirect to a page or show a message indicating unauthorized access
        return redirect('add_user')

    if request.method == 'POST':
        form = UserCreationFormExtended(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or show a success message
            return render(request, 'events/duty_alloc.html')
    else:
        form = UserCreationFormExtended()
    return render(request, 'events/add_user.html', {'form': form})


@login_required
@user_passes_test(admin_check)
def add_faculty(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'events/duty_alloc.html')  # Redirect to a page displaying the list of faculty members
    else:
        form = FacultyForm()
    return render(request, 'events/add_faculty.html', {'form': form})

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = addeventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = addeventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

def confirm_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events')
    return render(request, 'events/confirm_delete.html', {'event': event})


def delete_report(request, report_id):
    report = get_object_or_404(Event_Report, pk=report_id)
    report.delete()
    return redirect('report_page')


def edit_report(request, report_id):
    report = get_object_or_404(Event_Report, pk=report_id)
    if request.method == 'POST':
        form = EventReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report_page')
    else:
        form = EventReportForm(instance=report)
    return render(request, 'events/add_report.html', {'form': form, 'report': report})


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = addeventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = addeventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

def confirm_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('events')
