from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def admin_required(view_func):

    @login_required(login_url="auth_page")
    def wrapper(request, *args, **kwargs):

        if hasattr(request.user, "userprofile") and request.user.userprofile.role == "admin":
            return view_func(request, *args, **kwargs)

        messages.error(request, "You are not authorized to access admin panel.")
        return redirect("auth_page")

    return wrapper
