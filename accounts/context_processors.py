from providers.models import ProviderProfile

def pending_provider_count(request):

    if request.user.is_authenticated and hasattr(request.user, "userprofile"):
        if request.user.userprofile.role == "admin":
            count = ProviderProfile.objects.filter(status="pending").count()
            return {"pending_count": count}

    return {}