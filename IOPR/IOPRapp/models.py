from django.db import models

class Bamboo(models.Model):
    
    STATUS_CHOICES = (
        ('True', 'Active'),
    )
    
    Employee = models.IntegerField(null=True)
    FirstName = models.CharField(max_length=100, null=True)
    LastName = models.CharField(max_length=100, null=True)
    PreferredName = models.CharField(max_length=100, null=True)
    Status = models.CharField(max_length=100, default='Active', null=True)
    JobLevel = models.CharField(max_length=100, null=True)
    EmploymentStatus = models.CharField(max_length=100, null=True)	
    Location = models.CharField(max_length=100, null=True)	
    Division = models.CharField(max_length=100, null=True)	
    Department = models.CharField(max_length=100, null=True)	
    JobTitle = models.CharField(max_length=100, null=True)	
    ReportingTo	= models.CharField(max_length=100, null=True)
    WorkEmail = models.EmailField(max_length=254, null=False)
    JobInformation_Date = models.DateField(null=True)
    FirstNameLastName = models.CharField(max_length=100, null=True)
    SupervisorID = models.PositiveIntegerField(null=True)	
    Budgeter = models.CharField(max_length=100, null=True)	
    NetsuiteInternalID = models.IntegerField(null=True)		 
    EmploymentStatus_Date = models.DateField(null=True)	
    FTE = models.CharField(max_length=100, null=True)
    ResignationDate	= models.DateField(null=True)
    Product1 = models.CharField(max_length=100, null=True)
    Product2 = models.CharField(max_length=100, null=True)	
    Entity	= models.CharField(max_length=100, null=True)
    HireDate = models.DateField(null=True)	
    Tenure = models.CharField(max_length=100, null=True)
    TimeZoneOffsetValue = models.IntegerField(null=True)
    
    def __str__(self):
        return self.FirstNameLastName


class Weekly_Schedule(models.Model):
    reporting_to = models.CharField(max_length=100)
    employee = models.CharField(max_length=100)
    employeeID = models.CharField(max_length=1000, null=True)
    days = models.CharField(max_length=1000, null=True)
    week = models.CharField(max_length=10)
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - Week {self.week} - Date - {self.days}"
    
    def get_checked_days(self):
        checked_days = [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if getattr(self, day.lower())]
        return ', '.join(checked_days)
    
    def save(self, *args, **kwargs):
        # Update boolean fields based on the days field
        if self.days:
            checked_days = [day.strip() for day in self.days.split(',')]
            for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                setattr(self, day.lower(), day in checked_days)
        super().save(*args, **kwargs)

class Regular_Schedule(models.Model):
    reporting_to = models.CharField(max_length=100)
    employee = models.CharField(max_length=100)
    employeeID = models.CharField(max_length=1000, null=True)
    days = models.CharField(max_length=1000, null=True)
    week = models.CharField(max_length=10, null=True)
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - Week {self.week} - Days: {self.get_checked_days()}"

    def get_checked_days(self):
        checked_days = [day for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"] if getattr(self, day.lower())]
        return ', '.join(checked_days)
    

    def save(self, *args, **kwargs):
        # Update boolean fields based on the days field
        if self.days:
            checked_days = [day.strip() for day in self.days.split(',')]
            for day in ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
                setattr(self, day.lower(), day in checked_days)
        super().save(*args, **kwargs)
    

    
    



