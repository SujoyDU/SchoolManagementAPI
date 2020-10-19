from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff

class IsTeacherUser(permissions.BasePermission):

    def has_permission(self, request, view):
        isTeacher = False
        if(not request.user.is_superuser):
            if (request.user.profile.user_type) =='T':
                isTeacher = True
            return request.user and isTeacher
        else: return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        isTeacher = False
        if (not request.user.is_superuser):
            if (request.user.profile.user_type) == 'T':
                isTeacher = True
            return request.user and isTeacher
        else:
            return request.user and request.user.is_staff

class IsStudentUser(permissions.BasePermission):

    def has_permission(self, request, view):
        isTeacher = False
        if (not request.user.is_superuser):
            if (request.user.profile.user_type) == 'S':
                isTeacher = True
            return request.user and isTeacher
        else:
            return request.user and request.user.is_staff
    def has_object_permission(self, request, view, obj):
        isTeacher = False
        if (not request.user.is_superuser):
            if (request.user.profile.user_type) == 'S':
                isTeacher = True
            return request.user and isTeacher
        else:
            return request.user and request.user.is_staff
