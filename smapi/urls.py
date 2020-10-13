from django.conf.urls import url, include
from rest_framework import routers
from smapi.views import UserViewSet, DepartmentViewSet, InstructorViewSet, CourseViewSet,TeachesViewSet,StudentViewSet,TakesViewSet, StudentGradeViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'instructor', InstructorViewSet)
router.register(r'course', CourseViewSet)
router.register(r'teaches', TeachesViewSet)
router.register(r'student', StudentViewSet)
router.register(r'takes', TakesViewSet)
router.register(r'studentgrade', StudentGradeViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),

]