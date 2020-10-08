from django.conf.urls import url, include
from rest_framework import routers
from smapi.views import UserViewSet, DepartmentViewSet, InstructorViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'instructor', InstructorViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),

]