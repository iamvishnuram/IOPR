import json
from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Bamboo, Weekly_Schedule, Regular_Schedule
from datetime import datetime, timedelta
from .forms import WeekForm
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.azure.views import AzureOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

def microsoft_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    

    # Create an instance of the AzureOAuth2Adapter
    azure_adapter = AzureOAuth2Adapter(request)

    # Get the login URL for the Microsoft account
    login_url = azure_adapter.get_authorization_url(
        request,
        OAuth2Client.AUTHORIZATION_URL 
    )

    return render(request, 'login.html', {'microsoft': login_url})

def microsoft_callback(request):
    # Create an instance of the AzureOAuth2Adapter
    azure_adapter = AzureOAuth2Adapter(request)

    # Complete the authentication process
    token = azure_adapter.complete_login(request)

    # Retrieve the user's email from the SocialAccount model
    social_account = SocialAccount.objects.get(provider='microsoft', uid=token.account.uid)
    user = social_account.user

    login(request, user)

    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'Registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    today = datetime.now().date()
    weekday = today.weekday() 
    current_week = int(today.strftime('%W')) + 1
    start_date = today - timedelta(days=weekday)
    week = int(start_date.strftime('%W')) + 1  # Changed from %U to %W
    week_dates = [(start_date + timedelta(days=i)).strftime('%A, %b %d') for i in range(7)]

    weeks = []
    for i in range(-4, 2):
        week_start = (today + timedelta(days=7*i)) - timedelta(days=(today + timedelta(days=7*i)).weekday())
        week_end = week_start + timedelta(days=7)
        week_start_mod = week_start - timedelta(days=1)
        week_end_mod = week_end - timedelta(days=2)
        week_str = f"{week_start.strftime('%W')} ({week_start_mod.strftime('%d/%m/%Y')} - {week_end_mod.strftime('%d/%m/%Y')})"
        weeks.append((week_start.strftime('%W'), week_str))
    
    form = WeekForm()
    form.fields['week'].choices = [('','Choose a week')] + weeks
    print(weeks)

    # departments = Bamboo.objects.values_list('Department', flat=True).order_by('Department').distinct()
    managers = Bamboo.objects.values_list('ReportingTo', flat=True).order_by('ReportingTo').distinct()

    context = {'managers':managers, 'week': week, 'week_dates': week_dates, 'form': form}

    return render(request, 'home.html', context)

@login_required(login_url='login')
def load_weekly_employees(request):
    selected_manager = request.GET.get('manager')
    selected_week = request.GET.get('week')
    employees = Bamboo.objects.filter(ReportingTo=selected_manager)
    data = {
        'employees': [],
        'employeeID': [],
        'savedDates': []
    }

    for employee in employees:
        data['employees'].append(employee.FirstNameLastName)
        data['employeeID'].append(employee.Employee)

        # Fetch the saved dates for each employee from the Regular_Schedule model based on week
        saved_dates = Weekly_Schedule.objects.filter(employee=employee, week=selected_week)

        # Collect the checked dates based on the checkboxes
        saved_dates_list = []
        for entry in saved_dates:
            checked_days = [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if getattr(entry, day.lower())]
            saved_dates_list.extend(checked_days)

        data['savedDates'].append(saved_dates_list)
        # print(saved_dates_list)

    return JsonResponse(data, safe=False)

@login_required(login_url='login')
def load_regular_employees(request):
    selected_manager = request.GET.get('manager')
    employees = Bamboo.objects.filter(ReportingTo=selected_manager)
    data = {
        'employees': [],
        'employeeID': [],
        'savedDates': []
    }

    for employee in employees:
        data['employees'].append(employee.FirstNameLastName)
        data['employeeID'].append(employee.Employee)

        # Fetch the saved dates for each employee from the Regular_Schedule model
        saved_dates = Regular_Schedule.objects.filter(employee=employee)

        # Collect the checked dates based on the checkboxes
        saved_dates_list = []
        for entry in saved_dates:
            checked_days = [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if getattr(entry, day.lower())]
            saved_dates_list.extend(checked_days)

        data['savedDates'].append(saved_dates_list)
        # print(saved_dates_list)

    return JsonResponse(data, safe=False)


def week_dates(request):
    selected_week = request.GET.get('week')
    current_year = datetime.now().year
    start_date = datetime.strptime(f'{current_year}-W{selected_week}-1', '%G-W%V-%u').date()
    week_dates = [(start_date + timedelta(days=i-1)).strftime('%Y-%m-%d') for i in range(7)]
    print(week_dates)
    return JsonResponse({'week_dates': week_dates})

def save_weekly_schedule(request):
    if request.method == 'POST':
        reporting_to = request.POST.get('manager')
        week = request.POST.get('week')
        employees = set(request.POST.getlist('employee[]'))
        print(employees)
        employee_ids = []
        
        for employee in employees:
            bamboo_employee = get_object_or_404(Bamboo, FirstNameLastName=employee)
            employee_ids.append(bamboo_employee.Employee)
        print(employee_ids)
        
        days_json = request.POST.get('days')
        days = json.loads(days_json)
        
        manager = get_object_or_404(Bamboo, FirstNameLastName=reporting_to)
        reporting_to_email = manager.WorkEmail
        print(reporting_to_email)
        
        data = []
        for employee, employee_id in zip(employees, employee_ids):
            checked_days = [day for day in days[employee]]
            entry = {
                'reporting_manager': reporting_to,
                'employee': employee,
                'employee_id': employee_id,
                'week': week,
                'day': ", ".join(checked_days)
            }
            data.append(entry)
        print(data)

        html_message = render_to_string('email_template.html', {'data': data})
        
        if not employees:
            messages.error(request, 'Error: Required field not selected')
        else:
            for employee_id in employee_ids:
                Weekly_Schedule.objects.filter(
                employeeID=employee_id,
                week=week
            ).delete()

            for employee, employee_id in zip(employees, employee_ids):
                # Create a list of days that are checked for the current employee
                checked_days = [day for day in days[employee]]

                # Create a single Regular_Schedule object for the current employee and save it
                weekly = Weekly_Schedule(
                    reporting_to=reporting_to,
                    employee=employee,
                    employeeID=employee_id,
                    week=week,
                    days=", ".join(checked_days)
                )
                weekly.save()
                
            #Compose email
            subject = f'Inoffice Roaster Submission - Notification - Calendar Week No.{week}'

            # Create EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, to=['vishnu.m@kaseya.com'])
            email_message.attach_alternative(html_message, "text/html")
            
            email_message.send()
            

            messages.success(request, 'Weekly Schedule saved successfully!')
            return HttpResponse('Weekly Schedule saved successfully!')

    else:
        return HttpResponseBadRequest('Invalid request method')


def save_regular_schedules(request):
    today = datetime.now()
    weekday = today.weekday()
    start_date = today - timedelta(days=weekday)
    current_week = start_date.strftime('%W')
    if request.method == 'POST':
        reporting_to = request.POST.get('manager')
        week = request.POST.get('week')
        employees = set(request.POST.getlist('employee[]'))
        print(employees)
        employee_ids = []
        
        for employee in employees:
            bamboo_employee = get_object_or_404(Bamboo, FirstNameLastName=employee)
            employee_ids.append(bamboo_employee.Employee)
        print(employee_ids)
        
        days_json = request.POST.get('days')
        days = json.loads(days_json)
        
        manager = get_object_or_404(Bamboo, FirstNameLastName=reporting_to)
        reporting_to_email = manager.WorkEmail
        print(reporting_to_email)
        
        data = []
        for employee, employee_id in zip(employees, employee_ids):
            checked_days = [day for day in days[employee]]
            entry = {
                'reporting_manager': reporting_to,
                'employee': employee,
                'employee_id': employee_id,
                'week': week,
                'day': ", ".join(checked_days)
            }
            data.append(entry)
        print(data)

        html_message = render_to_string('email_template.html', {'data': data})
        
        if not employees:
            messages.error(request, 'Error: Required field not selected')
        else:
            for employee_id in employee_ids:
                Weekly_Schedule.objects.filter(
                employeeID=employee_id,
                week=week
            ).delete()
            
            for employee_id in employee_ids:    
                Regular_Schedule.objects.filter(
                    employeeID=employee_id,
                ).delete()

            for employee, employee_id in zip(employees, employee_ids):
                # Create a list of days that are checked for the current employee
                checked_days = [day for day in days[employee]]

                # Create a single Regular_Schedule object for the current employee and save it
                if week == current_week:
                    regular = Regular_Schedule(
                        reporting_to=reporting_to,
                        employee=employee,
                        employeeID=employee_id,
                        days=", ".join(checked_days)
                    )
                    regular.save()
                    
                    weekly = Weekly_Schedule(
                        reporting_to=reporting_to,
                        week = week,
                        employee=employee,
                        employeeID=employee_id,
                        days=", ".join(checked_days)
                    )
                    weekly.save()
                else:
                    regular = Regular_Schedule(
                        reporting_to=reporting_to,
                        employee=employee,
                        employeeID=employee_id,
                        days=", ".join(checked_days)
                    )
                    regular.save()
            #Compose email
            subject = f'Inoffice Roaster Submission - Notification - Calendar Week No.{week}'
            body = f'Hello, This is a notification for your Inoffice Presence Roaster submission for the mentioned calendar week. Please find the attached details.\n\nReporting Manager: {reporting_to}\n\nWeek No: {week}'
            # Create EmailMultiAlternatives object
            email_message = EmailMultiAlternatives(subject, body, to=['vishnuram80@gmail.com'])
            email_message.attach_alternative(html_message, "text/html")
            
            email_message.send()
            

            messages.success(request, 'Regular_Schedule saved successfully!')
            return HttpResponse('Regular_Schedule saved successfully!')

    else:
        return HttpResponseBadRequest('Invalid request method')

