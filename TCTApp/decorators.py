from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden

# Decorator for restricting access to admin-only views
def admin_only(view_func):
    # Decorate the view function with staff_member_required decorator
    decorated_view_func = staff_member_required(view_func)

    # Define a new function to check if the user is an admin
    def check_admin(request, *args, **kwargs):
        # Check if the user is not a staff member
        if not request.user.is_staff:
            # If not, return a forbidden response
            return HttpResponseForbidden()
        
        # If the user is a staff member, invoke the decorated view function
        return decorated_view_func(request, *args, **kwargs)

    # Return the new function as the updated view function
    return check_admin
