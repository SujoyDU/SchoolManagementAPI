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

create table teaches
	(ID			varchar(5), 
	 course_id		varchar(8),
	 sec_id			varchar(8), 
	 semester		varchar(6),
	 year			numeric(4,0),
	 primary key (ID, course_id, sec_id, semester, year),
	 foreign key (course_id, sec_id, semester, year) references section (course_id, sec_id, semester, year)
		on delete cascade,
	 foreign key (ID) references instructor (ID)
		on delete cascade
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

    def __str__(self):
        return "{}".format(self.tid)

class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key= True)
    course_name = models.CharField(max_length=255)
    dept_name = models.OneToOneField(Department,on_delete=models.CASCADE, related_name='dept')
    credits = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00), MaxValueValidator(12.00)])
    def __str__(self):
        return "{course_id} {course_name}".format(course_id = self.course_id,course_name=self.course_name)


class Teaches(models.Model):
    tid = models.ForeignKey(Instructor,on_delete=models.CASCADE, related_name='teacher')
    course_id = models.ForeignKey(Course,related_name='teachcourse',on_delete=models.CASCADE)

    # tid = models.CharField(max_length=10)
    # course_id = models.CharField(max_length=10)

    semester_time = [
        ('Fa', 'Fall'),
        ('Su', 'Summer'),
        ('Wi', 'Winter'),
        ('Sp', 'Spring'),
    ]
    semester = models.CharField(
        max_length=10,
        choices=semester_time,
        default='Fall',
    )
    year = models.DateField(null=True)
    def __str__(self):
        return "{tid} {course_id} {semester} {year}".format(tid = self.tid,course_id=self.course_id,semester=self.semester,year=self.year)


'''
create table student
	(ID			varchar(5), 
	 name			varchar(20) not null, 
	 dept_name		varchar(20), 
	 tot_cred		numeric(3,0) check (tot_cred >= 0),
	 primary key (ID),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);


create table takes
	(ID			varchar(5), 
	 course_id		varchar(8),
	 sec_id			varchar(8), 
	 semester		varchar(6),
	 year			numeric(4,0),
	 grade		        varchar(2),
	 primary key (ID, course_id, sec_id, semester, year),
	 foreign key (course_id, sec_id, semester, year) references section (course_id, sec_id, semester, year)
		on delete cascade,
	 foreign key (ID) references student (ID)
		on delete cascade
	);

create table student_cgpa
    (
        s_id
        cgpa
    )

calculate cgpa
calculate semester cgpa
calculate gpa

'''

class Student(models.Model):
    uid = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    sid = models.CharField(max_length=10, unique= True, primary_key=True)
    dept_name = models.OneToOneField(Department,on_delete=models.CASCADE, related_name='studept')
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00)])

    def __str__(self):
        return "{}".format(self.sid)



class Takes(models.Model):
    sid = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='stu')
    course_id = models.ForeignKey(Course, related_name='takescourse', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teaches, related_name='teacher',on_delete=models.CASCADE)
    semester_time = [
        ('Fa', 'Fall'),
        ('Su', 'Summer'),
        ('Wi', 'Winter'),
        ('Sp', 'Spring'),
    ]
    semester = models.CharField(
        max_length=10,
        choices=semester_time,
        default='Fall',
    )

    course_def = [
        ('C','Current'),
        ('F','FAIL'),
        ('P', 'PASS'),
        ('W','WITHDRAW'),
        ('T','TAKEN')
    ]

    year = models.DateField(null=True)
    course_marks = models.PositiveIntegerField(null=True)
    course_status = models.CharField(choices=course_def, max_length=10, default='Current')
    gpa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00)])

    @property
    def course_grade(self):
        if self.course_status == 'WITHDRAW':
            return 'W'
        if self.course_status == 'CURRENT':
            return 'N/A'
        if self.course_status == 'TAKEN':
            if self.course_marks >= 93:
                return 'A'
            elif self.course_marks >= 90:
                return 'A-'
            elif self.course_marks >= 87:
                return 'B+'
            else:
                return 'F'

    @property
    def course_gpa(self):
        if self.course_status == 'WITHDRAW':
            return -1
        if self.course_status == 'CURRENT':
            return -2
        if self.course_status == 'TAKEN':
            if self.course_grade == 'A':
                return 4.00
            if self.course_grade == 'A-':
                return 3.50

            if self.course_grade == 'B+':
                return 3.00
            if self.course_grade == 'F':
                return 0.00

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'semester', 'year'], name='unique_course_time'),
        ]


    def __str__(self):
        return "{sid} {course_id} {semester} {year}".format(tid = self.tid,course_id=self.course_id,semester=self.semester,year=self.year)



class StudentGrades(models.Model):
    tid = models.ForeignKey(Teaches, on_delete=models.CASCADE, related_name='teach')
    students = models.ManyToManyField(Takes,related_name='takes')
    course_name = models.ForeignKey(Course,related_name='course',on_delete=models.CASCADE)
    def __str__(self):
        return "{tid} {students}".format(tid = self.tid, students= self.students)