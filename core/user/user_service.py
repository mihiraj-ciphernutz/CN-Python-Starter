from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.base.base_service import BaseService
from core.user.user_database import UserDatabase

class UserService(BaseService):
    def __init__(self):
        super().__init__(UserDatabase)

    @csrf_exempt
    def login_view(request):
        if request.user.is_authenticated:
            return JsonResponse({"message": "User is already logged in."}, status=200)

        if request.method == 'POST':
                data = json.loads(request.body)
                email = data.get('email')
                password = data.get('password')

                if not email or not password:
                    return JsonResponse({'error': 'Email and password are required'}, status=400)
                
                user = authenticate(username=email, password=password)  
                if user:
                    login(request, user)
                    return JsonResponse({"message": "Login successful"})

                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    @csrf_exempt
    def logout_view(request):
         if not request.user.is_authenticated:
            return JsonResponse({"message": "User is already logged out."}, status=400)
        
         logout(request)
         return JsonResponse({"message":"Logout successful"})
    
# methods = [attr for attr in dir(UserService) if callable(getattr(UserService, attr)) and not attr.startswith('__')]
# print(methods)