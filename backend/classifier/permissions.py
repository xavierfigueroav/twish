"""
This module contains custom permission classes to grant or deny user access
depending on different business concerns.

The custom permission classes are:
    * AppConfiguredPermission - It grants access only if the application is
    configured when a request arrives.
"""
from rest_framework import permissions

from .models import App


class AppConfiguredPermission(permissions.BasePermission):
    """
    Custom permission class to grant or deny access to any user based on
    whether the application has been configured or not.

    Attributes
    ----------
    message : str
        Response message to return after a request is denied.
    """

    def has_permission(self, request, view):
        """
        This method grants access only if the application is configured when
        the request gets in.

        Parameters
        ----------
        request : rest_framework.request.Request
            It contains information about the request made by the user.
        view : DRF WrappedAPIView
            The target view (from views.py) to handle the request.

        Returns
        -------
        bool
            True (grant request) when there exists an instance of the model
            App (i.e. the app is configured), otherwise False (deny request).
        """

        self.message = f'Application has not been yet configured. \
Go to http://{request.get_host()}/admin and create an instance of App model'
        return App.objects.count() > 0
