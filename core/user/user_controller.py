from django.urls import path
from core.user.user_service import UserService
from core.base.base_controller import BaseController

class UserController(BaseController):
    def __init__(self):
        super().__init__(UserService)

user_controller = UserController()

urlpatterns = user_controller.get_urls()

urlpatterns += [
    path('login/', UserService.login_view, name='login'),
    path('logout/', UserService.logout_view, name='logout')
]

# for url in urlpatterns:
#     print(url)