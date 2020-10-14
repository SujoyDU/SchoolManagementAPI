from rest_framework import serializers
from smapi.models import User, UserProfile, Department, Instructor, Course, Teaches, Student,Takes,Section


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user_type','title', 'dob', 'address', 'country', 'city', 'zip', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.StringRelatedField(many=True)
    instructors = serializers.StringRelatedField(many=True)
    deptstudents = serializers.StringRelatedField(many=True)
    class Meta:
        model = Department
        fields = ('dept_name','building','budget','course','instructors','deptstudents')


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    # uid = UserSerializer(required=True)
    class Meta:
        model = Instructor
        fields = ('uid','tid','dept_name', 'salary')

    def create(self, validated_data):
        instructor = Instructor(**validated_data)
        instructor.save()
        return instructor

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id','course_name','dept_name','credits')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class TeachesSerializer(serializers.HyperlinkedModelSerializer):
    totalstudents = serializers.HyperlinkedRelatedField(many=True,queryset=Takes.objects.all(),view_name='takes-detail')
    class Meta:
        model = Teaches
        fields = ('tid','teachcourse','totalstudents')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    # uid = UserSerializer(required=True)
    class Meta:
        model = Student
        fields = ('uid','sid','dept_name', 'total_credit')

    def create(self, validated_data):
        student = Student(**validated_data)
        student.save()
        return student

class TakesSerializer(serializers.HyperlinkedModelSerializer):
    # course_grade = serializers.ReadOnlyField()
    # course_gpa = serializers.ReadOnlyField()
    course_grade = serializers.SerializerMethodField(method_name='calculate_grade')
    course_gpa = serializers.SerializerMethodField(method_name='calculate_course_gpa')
    class Meta:
        model = Takes
        fields = "__all__"

    def calculate_grade(self,instance):
        if instance.course_status == 'W':
            return 'W'
        if instance.course_status == 'C' and instance.course_marks < 0:
            return 'N/A'
        if instance.course_status == 'C' and instance.course_marks > -1:
            if instance.course_marks >= 93:
                return 'A'
            elif instance.course_marks >= 90:
                return 'A-'
            elif instance.course_marks >= 87:
                return 'B+'
            elif instance.course_marks >= 80:
                return 'B'
            elif instance.course_marks >= 70:
                return 'D'
            else:
                return 'F'

    def calculate_course_gpa(self, instance):
        if instance.course_status == 'W':
            return 0.00
        if instance.course_status == 'C' and instance.course_marks < 0:
            return 0.00
        if instance.course_status == 'C' and instance.course_marks > -1:
            if instance.course_marks >= 93:
                return 4.00
            elif instance.course_marks >= 90:
                return 3.85
            elif instance.course_marks >= 87:
                return 3.70
            elif instance.course_marks >= 80:
                return 3.50
            elif instance.course_marks >= 70:
                return 3.00
            else:
                return 0.00

# class StudentGradesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = StudentGrades
#         fields = "__all__"