from django.contrib import admin
from .models import Bamboo, Weekly_Schedule, Regular_Schedule
from import_export.admin import ImportExportModelAdmin
from datetime import datetime,timedelta

class BambooAdmin(ImportExportModelAdmin):
    list_display = ['FirstNameLastName']
    list_filter = ['ReportingTo']
admin.site.register(Bamboo, BambooAdmin)

class Regular_ScheduleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('employeeID', 'employee', 'reporting_to', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    
admin.site.register(Regular_Schedule, Regular_ScheduleAdmin)

class Weekly_ScheduleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('employeeID', 'employee', 'reporting_to', 'week','sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    list_filter = ['week']
admin.site.register(Weekly_Schedule, Weekly_ScheduleAdmin)


