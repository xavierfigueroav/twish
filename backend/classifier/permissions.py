from rest_framework import permissions

from .models import App


class AppConfiguredPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        self.message = f'Application has not been yet configured. \
Go to http://{request.get_host()}/admin and create an instance of App model'
        return App.objects.count() > 0
