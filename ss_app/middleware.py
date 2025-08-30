from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated and is the specific testadmin
        if request.user.is_authenticated and request.user.username == 'testadmin':
            # List of URLs that testadmin can access
            admin_allowed_urls = [
                '/custom-admin/',
                '/admin/',
                '/accounts/logout/',
                '/logout/',
                '/admin_logout/',
            ]
            
            # Check if current path is not in admin allowed URLs
            current_path = request.path
            is_admin_url = any(current_path.startswith(url) for url in admin_allowed_urls)
            
            # If testadmin tries to access regular site (including home page), redirect to admin dashboard
            if not is_admin_url:
                return redirect('admin_dashboard')
        
        response = self.get_response(request)
        return response
