# Generated by Django 4.2.6 on 2024-02-05 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bamboo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Employee', models.IntegerField(null=True)),
                ('FirstName', models.CharField(max_length=100, null=True)),
                ('LastName', models.CharField(max_length=100, null=True)),
                ('PreferredName', models.CharField(max_length=100, null=True)),
                ('Status', models.CharField(default='Active', max_length=100, null=True)),
                ('JobLevel', models.CharField(max_length=100, null=True)),
                ('EmploymentStatus', models.CharField(max_length=100, null=True)),
                ('Location', models.CharField(max_length=100, null=True)),
                ('Division', models.CharField(max_length=100, null=True)),
                ('Department', models.CharField(max_length=100, null=True)),
                ('JobTitle', models.CharField(max_length=100, null=True)),
                ('ReportingTo', models.CharField(max_length=100, null=True)),
                ('WorkEmail', models.EmailField(max_length=254)),
                ('JobInformation_Date', models.DateField(null=True)),
                ('FirstNameLastName', models.CharField(max_length=100, null=True)),
                ('SupervisorID', models.PositiveIntegerField(null=True)),
                ('Budgeter', models.CharField(max_length=100, null=True)),
                ('NetsuiteInternalID', models.IntegerField(null=True)),
                ('EmploymentStatus_Date', models.DateField(null=True)),
                ('FTE', models.CharField(max_length=100, null=True)),
                ('ResignationDate', models.DateField(null=True)),
                ('Product1', models.CharField(max_length=100, null=True)),
                ('Product2', models.CharField(max_length=100, null=True)),
                ('Entity', models.CharField(max_length=100, null=True)),
                ('HireDate', models.DateField(null=True)),
                ('Tenure', models.CharField(max_length=100, null=True)),
                ('TimeZoneOffsetValue', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Regular_Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporting_to', models.CharField(max_length=100)),
                ('employee', models.CharField(max_length=100)),
                ('employeeID', models.CharField(max_length=1000, null=True)),
                ('days', models.CharField(max_length=1000, null=True)),
                ('week', models.CharField(max_length=10, null=True)),
                ('sunday', models.BooleanField(default=False)),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Weekly_Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporting_to', models.CharField(max_length=100)),
                ('employee', models.CharField(max_length=100)),
                ('employeeID', models.CharField(max_length=1000, null=True)),
                ('days', models.CharField(max_length=1000, null=True)),
                ('week', models.CharField(max_length=10)),
                ('sunday', models.BooleanField(default=False)),
                ('monday', models.BooleanField(default=False)),
                ('tuesday', models.BooleanField(default=False)),
                ('wednesday', models.BooleanField(default=False)),
                ('thursday', models.BooleanField(default=False)),
                ('friday', models.BooleanField(default=False)),
                ('saturday', models.BooleanField(default=False)),
            ],
        ),
    ]