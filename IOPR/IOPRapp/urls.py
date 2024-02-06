from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.index, name='home'),
    path('load_employees/', views.load_weekly_employees, name='load_employees'),
    path('load_regular_employees/', views.load_regular_employees, name='load_regular_employees'),
    path('week_dates/', views.week_dates, name='week_dates'),
    path('save_roster/', views.save_weekly_schedule, name='save_weekly_schedule'),
    path('save_regular_schedule/', views.save_regular_schedules, name='save_regular_schedules'),
    path('microsoft/login/', views.microsoft_login, name='microsoft_login'),
    path('microsoft/callback/', views.microsoft_callback, name='microsoft_callback'),
]