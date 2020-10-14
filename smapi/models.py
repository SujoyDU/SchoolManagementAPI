from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CheckConstraint, Q
import datetime
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


class Department(models.Model):
    dept_name = models.CharField(max_length=255, primary_key=True)
    building = models.CharField(max_length=255)
    budget = models.PositiveIntegerField()
    def __str__(self):
        return "{}".format(self.dept_name)


class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key= True)
    course_name = models.CharField(max_length=255)
    dept_name = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='course')
    credits = models.FloatField(default=0.00,validators=[MinValueValidator(0.00), MaxValueValidator(12.00)])
    def __str__(self):
        return "{course_id} {course_name} {credits}".format(course_id = self.course_id,course_name=self.course_name,credits = self.credits)


class Instructor(models.Model):
    uid = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher')
    tid = models.CharField(max_length=10, unique= True, primary_key=True)
    dept_name = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='instructors')
    designation = models.CharField(max_length=255, default='Lecturer')
    salary = models.FloatField(validators=[MinValueValidator(29000), MaxValueValidator(300000)])

    def __str__(self):
        return "{tid} {dept_name}".format(tid=self.tid, dept_name = self.dept_name)

class Student(models.Model):
    uid = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student')
    sid = models.CharField(max_length=10, unique= True, primary_key=True)
    dept_name = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='deptstudents')
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,validators=[MinValueValidator(0.00)])

    def __str__(self):
        return "{}".format(self.sid)

class Section(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cid')
    sec_id = models.CharField(max_length=10)
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
    year = models.DateField(default=datetime.date.today().year, null=True)

    def __str__(self):
        return "{sec_id} {course_id} {semester} {year}".format(sec_id=self.sec_id, course_id=self.course_id,
                                                            semester=self.semester, year=self.year)

    class Meta:
        unique_together = ['course_id', 'sec_id','semester', 'year']
        ordering = ['year']




class Teaches(models.Model):
    tid = models.ForeignKey(Instructor,on_delete=models.CASCADE, related_name='teacher')
    teachcourse = models.ForeignKey(Section,related_name='teachcourse',on_delete=models.CASCADE)

    # tid = models.CharField(max_length=10)
    # course_id = models.CharField(max_length=10)


    def __str__(self):
        return "{tid} {teachcourse}".format(tid = self.tid,teachcourse=self.teachcourse)





class Takes(models.Model):
    sid = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='stu')
    take_course = models.ForeignKey(Teaches,on_delete=models.CASCADE,related_name='totalstudents')

    course_def = [
        ('C','Current'),
        ('F','FAIL'),
        ('P', 'PASS'),
        ('W','WITHDRAW'),
    ]
    course_marks = models.FloatField(default=-1)
    course_status = models.CharField(choices=course_def, max_length=10, default='Current')

    def __str__(self):
        return "{sid}".format(sid = self.sid)

    class Meta:
        unique_together = ['sid', 'take_course']

