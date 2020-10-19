from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from smapi.models import User
from smapi.serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from smapi.models import User,Department,Instructor, Course,Teaches,Student,Takes,Section, Exam, GiveExam,GiveMarks
from smapi.serializers import UserSerializer, DepartmentSerializer,InstructorSerializer, CourseSerializer,TeachesSerializer,StudentSerializer,TakesSerializer,SectionSerializer
from smapi.serializers import ExamSerializer,GiveExamSerializer, GiveMarksSerializer
# Also add these imports
from smapi.permissions import IsLoggedInUserOrAdmin, IsAdminUser, IsStudentUser,IsTeacherUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list' :
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

# class UserProfileViewset(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#

class DepartmentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]

    # # Add this code block
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [AllowAny]
    #     elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
    #         permission_classes = [IsLoggedInUserOrAdmin]
    #     elif self.action == 'list' or self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

class InstructorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    # # Add this code block

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsTeacherUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsTeacherUser]
        return [permission() for permission in permission_classes]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]


class TeachesViewSet(viewsets.ModelViewSet):
    queryset = Teaches.objects.all()
    serializer_class = TeachesSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacherUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsTeacherUser]
        return [permission() for permission in permission_classes]


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # # Add this code block

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsStudentUser]
        return [permission() for permission in permission_classes]


class TakesViewSet(viewsets.ModelViewSet):
    queryset = Takes.objects.all()
    serializer_class = TakesSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsStudentUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsStudentUser]
        return [permission() for permission in permission_classes]



class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacherUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsTeacherUser]
        return [permission() for permission in permission_classes]


class GiveExamViewSet(viewsets.ModelViewSet):
    queryset = GiveExam.objects.all()
    serializer_class = GiveExamSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsStudentUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsStudentUser]
        return [permission() for permission in permission_classes]

class GiveMarksViewSet(viewsets.ModelViewSet):
    queryset = GiveMarks.objects.all()
    serializer_class = GiveMarksSerializer

    # Add this code block
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsTeacherUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'list':
            permission_classes = [IsTeacherUser]
        return [permission() for permission in permission_classes]


# class StudentGradeViewSet(viewsets.ModelViewSet):
#     queryset = Takes.objects.all()
#     serializer_class = TakesSerializer
#
#     def get_permissions(self):
#         permission_classes = []
#         if self.action == 'create':
#             permission_classes = [IsAdminUser]
#         elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
#             permission_classes = [IsLoggedInUserOrAdmin]
#         elif self.action == 'list' or self.action == 'destroy':
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]