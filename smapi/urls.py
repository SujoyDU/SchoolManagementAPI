from django.conf.urls import url, include
from rest_framework import routers
from smapi.views import UserViewSet, DepartmentViewSet, InstructorViewSet, CourseViewSet,TeachesViewSet,StudentViewSet,TakesViewSet,SectionViewSet
from smapi.views import ExamViewSet,GiveExamViewSet,GiveMarksViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'instructor', InstructorViewSet)
router.register(r'student', StudentViewSet)
router.register(r'course', CourseViewSet)
router.register(r'section',SectionViewSet)
router.register(r'teaches', TeachesViewSet)
router.register(r'takes', TakesViewSet)
router.register(r'exam', ExamViewSet)
router.register(r'giveexam', GiveExamViewSet)
router.register(r'markexam', GiveMarksViewSet)

# router.register(r'studentgrade', StudentGradeViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),

]