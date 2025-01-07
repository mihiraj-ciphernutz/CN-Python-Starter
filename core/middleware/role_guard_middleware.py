from django.http import JsonResponse

class RoleGuardMiddleware:
    """
    Middleware to ensure the user has the required permissions based on the is_owner flag.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        unrestricted_endpoints = [
            '/user/login/',
            '/user/logout/',
            '/user/create/',
        ]

        if request.path in unrestricted_endpoints:
            return self.get_response(request)

        owner_only_endpoints = [
            '/organization/create/', 
            '/organization/invite/',
        ]

        for endpoint in owner_only_endpoints:
            if request.path.startswith(endpoint):
                if not request.user.is_authenticated:
                    return JsonResponse({'error': 'Authentication required.'}, status=401)

                if not request.user.is_owner:
                    return JsonResponse({'error': 'Only owners can access this resource.'}, status=403)

        return self.get_response(request)