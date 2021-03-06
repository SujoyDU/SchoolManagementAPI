from rest_framework import serializers
from smapi.models import User, UserProfile, Department, Instructor, Course, Teaches, Student,Takes,Section, Exam, GiveExam, GiveMarks


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
    course = serializers.StringRelatedField(many=True, read_only=True)
    instructors = serializers.StringRelatedField(many=True, read_only=True)
    deptstudents = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Department
        fields = ('dept_name','building','budget','course','instructors','deptstudents')


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    # uid = UserSerializer(required=True)
    current_user = serializers.SerializerMethodField('_user')
    class Meta:
        model = Instructor
        fields = ('uid','tid','dept_name','designation','salary','current_user')

    def create(self, validated_data):
        instructor = Instructor(**validated_data)
        instructor.save()
        return instructor

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.pk

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('course_id','course_name','dept_name','credits')


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    # teachers = serializers.HyperlinkedRelatedField(many=True,queryset=Teaches.objects.all(),view_name='teaches-detail')
    # students = serializers.HyperlinkedRelatedField(many=True,queryset=Takes.objects.all(),view_name='takes-detail')
    class Meta:
        model = Section
        fields = '__all__'

class TeachesSerializer(serializers.HyperlinkedModelSerializer):
    # totalstudents = serializers.HyperlinkedRelatedField(many=True,queryset=Takes.objects.all(),view_name='takes-detail')
    # giveGrades = serializers.SerializerMethodField(method_name='calculate_credits')
    studentList = serializers.SerializerMethodField(method_name='get_students')
    current_user = serializers.SerializerMethodField('_user')
    class Meta:
        model = Teaches
        fields = '__all__'

    def get_students(self,request):
        students = Takes.objects.filter(take_course=request.teachcourse).values('sid')
        return students;

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            if(hasattr(request.user,'teacher')):
                if(hasattr(request.user.teacher,'pk')):
                    return request.user.teacher.pk
            else: return request.user.email
    # def give_grade(self,request):


class StudentSerializer(serializers.HyperlinkedModelSerializer):

    total_credit = serializers.SerializerMethodField(method_name='calculate_credits')
    class Meta:
        model = Student
        fields = ('uid','sid','dept_name','total_credit')

    def create(self, validated_data):
        student = Student(**validated_data)
        student.save()
        return student

    def calculate_credits(self, request):
        total_credit = 0.00
        takes_courses = Takes.objects.filter(sid=request.pk)
        for tc in takes_courses:
            total_credit += tc.take_course.course_id.credits
        return total_credit




class TakesSerializer(serializers.HyperlinkedModelSerializer):
    current_user = serializers.SerializerMethodField('_user')
    section = serializers.SerializerMethodField('getSection')
    course_grade = serializers.ReadOnlyField()
    course_gpa = serializers.ReadOnlyField()
    course_marks = serializers.SerializerMethodField(method_name='get_marks')
    course_grade = serializers.SerializerMethodField(method_name='calculate_grade')
    course_gpa = serializers.SerializerMethodField(method_name='calculate_course_gpa')
    class Meta:
        model = Takes
        fields = "__all__"

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            if(hasattr(request.user,'student')):
                if(hasattr(request.user.student,'pk')):
                    return request.user.student.pk
            else: return request.user.email

    def getSection(self, request):
        if (hasattr(request, 'take_course_id')):
            return request.take_course_id

    def get_marks(self,request):
        # if(GiveExam.objects.filter(student=request)):
        #     return GiveExam.objects.filter(student=request)[0].examobj.exam_marks
        if(hasattr(request,'takesstudent')):
            if(hasattr(request.takesstudent,'examobj')):
                if(hasattr(request.takesstudent.examobj,'exam_marks')):
                    return request.takesstudent.examobj.exam_marks
                else: return -1.00


    def calculate_grade(self,instance):
        if instance.course_status == 'W':
            return 'W'
        # if instance.course_status == 'C' and instance.course_marks < 0:
        #     return 'N/A'
        if (hasattr(instance,'takesstudent')):
            if(hasattr(instance.takesstudent,'examobj')):
                if(hasattr(instance.takesstudent.examobj,'exam_marks')):
                    if instance.takesstudent.examobj.exam_marks >= 93:
                        return 'A'
                    elif instance.takesstudent.examobj.exam_marks >= 90:
                        return 'A-'
                    elif instance.takesstudent.examobj.exam_marks >= 87:
                        return 'B+'
                    elif instance.takesstudent.examobj.exam_marks >= 80:
                        return 'B'
                    elif instance.takesstudent.examobj.exam_marks >= 70:
                        return 'D'
                    else:
                        return 'F'



    def calculate_course_gpa(self, instance):
        if instance.course_status == 'W':
            return 0.00
        # if instance.course_status == 'C' and instance.course_marks < 0:
        #     return 0.00
        if (hasattr(instance,'takesstudent')):
            if(hasattr(instance.takesstudent,'examobj')):
                if(hasattr(instance.takesstudent.examobj,'exam_marks')):
                    if instance.takesstudent.examobj.exam_marks >= 93:
                        return 4.00
                    elif instance.takesstudent.examobj.exam_marks >= 90:
                        return 3.85
                    elif instance.takesstudent.examobj.exam_marks >= 87:
                        return 3.70
                    elif instance.takesstudent.examobj.exam_marks >= 80:
                        return 3.50
                    elif instance.takesstudent.examobj.exam_marks >= 70:
                        return 3.00
                    else:
                        return 0.00


class ExamSerializer(serializers.HyperlinkedModelSerializer):

    current_user = serializers.SerializerMethodField('_user')
    exam_assigner = serializers.SerializerMethodField('getAssigner')
    section = serializers.SerializerMethodField('getSection')
    class Meta:
        model = Exam
        fields = "__all__"

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            if(hasattr(request.user,'teacher')):
                if(hasattr(request.user.teacher,'pk')):
                    return request.user.teacher.pk
            else: return request.user.email

    def getAssigner(self, request):
        # request = self.context.get('request', None)
        # request.teacher.tid_id
        if (hasattr(request, 'teacher')):
            if (hasattr(request.teacher, 'tid_id')):
                return request.teacher.tid_id

    def getSection(self, request):
        if (hasattr(request, 'teacher')):
            if (hasattr(request.teacher, 'teachcourse_id')):
                return request.teacher.teachcourse_id


class GiveExamSerializer(serializers.HyperlinkedModelSerializer):
    exam_assigner = serializers.SerializerMethodField('getAssigner')
    section = serializers.SerializerMethodField('getSection')
    current_user = serializers.SerializerMethodField('_user')
    class Meta:
        model = GiveExam
        fields = "__all__"

    # request.stuexam.teacher.tid_id
    def getAssigner(self, request):
        if(hasattr(request,'stuexam')):
            if (hasattr(request.stuexam, 'teacher')):
                if (hasattr(request.stuexam.teacher, 'tid_id')):
                    return request.stuexam.teacher.tid_id

    def getSection(self, request):
        if (hasattr(request,'student')):
            if (hasattr(request.student, 'take_course_id')):
                return request.student.take_course_id

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            if(hasattr(request.user,'student')):
                if(hasattr(request.user.student,'pk')):
                    return request.user.student.pk
            else: return request.user.email

    def validate(self, request):
        if(request['stuexam'].teacher.teachcourse == request['student'].take_course):
            return request
        else: raise serializers.ValidationError("Validation Error")



class GiveMarksSerializer(serializers.HyperlinkedModelSerializer):
    section = serializers.SerializerMethodField('getSection')
    exam_assigner = serializers.SerializerMethodField('get_tid')
    student_id = serializers.SerializerMethodField(method_name='get_student_id')
    current_user = serializers.SerializerMethodField('_user')
    class Meta:
        model = GiveMarks
        fields = "__all__"
    # request.examobj.student.take_course_id
    def getSection(self, request):
        if (hasattr(request,'examobj')):
            if (hasattr(request.examobj, 'student')):
                if (hasattr(request.examobj.student, 'take_course_id')):
                    return request.examobj.student.take_course_id


    def get_student_id(self,request):

        return request.examobj.student.sid.sid;
        pass
    # obj.examobj.stuexam.teacher.tid_id
    def get_tid(self,request):
        return request.examobj.stuexam.teacher.tid_id

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            if(hasattr(request.user,'teacher')):
                if(hasattr(request.user.teacher,'pk')):
                    return request.user.teacher.pk
            else: return request.user.email


# class StudentGradesSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = StudentGrades
#         fields = "__all__"