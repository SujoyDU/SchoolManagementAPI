from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    user_types = [
        ('S','Student'),
        ('T', 'Teacher'),
        ('N', 'None'),
    ]
    user_type = models.CharField(
        max_length=10,
        choices=user_types,
        default='None',
    )
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)

'''
create table instructor
	(ID			varchar(5), 
	 name			varchar(20) not null, 
	 dept_name		varchar(20), 
	 salary			numeric(8,2) check (salary > 29000),
	 primary key (ID),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);
	
create table department
	(dept_name		varchar(20), 
	 building		varchar(15), 
	 budget		        numeric(12,2) check (budget > 0),
	 primary key (dept_name)
	);

create table course
	(course_id		varchar(8), 
	 title			varchar(50), 
	 dept_name		varchar(20),
	 credits		numeric(2,0) check (credits > 0),
	 primary key (course_id),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);

create table section
	(course_id		varchar(8), 
         sec_id			varchar(8),
	 semester		varchar(6)
		check (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
	 year			numeric(4,0) check (year > 1701 and year < 2100), 
	 building		varchar(15),
	 room_number		varchar(7),
	 time_slot_id		varchar(4),
	 primary key (course_id, sec_id, semester, year),
	 foreign key (course_id) references course (course_id)
		on delete cascade,
	 foreign key (building, room_number) references classroom (building, room_number)
		on delete set null
	);


'''
class Department(models.Model):
    dept_name = models.CharField(max_length=255, primary_key=True)
    building = models.CharField(max_length=255)
    budget = models.PositiveIntegerField()
    def __str__(self):
        return "{}".format(self.dept_name)

class Instructor(models.Model):
    uid = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor')
    tid = models.CharField(max_length=10, unique= True, primary_key=True)
    dept_name = models.OneToOneField(Department,on_delete=models.CASCADE, related_name='department')
    designation = models.CharField(max_length=255, default='Lecturer')
    salary = models.PositiveIntegerField(validators=[MinValueValidator(29000), MaxValueValidator(300000)])

class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key= True)
    title = models.CharField(max_length=255)
    dept_name = models.OneToOneField(Department,on_delete=models.CASCADE, related_name='dept')
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00), MaxValueValidator(12.00)])

