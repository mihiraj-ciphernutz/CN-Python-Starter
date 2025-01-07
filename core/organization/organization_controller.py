from django.urls import path
from core.base.base_controller import BaseController
from core.organization.organization_service import OrganizationService

class OrgnizationController(BaseController):
    def __init__(self):
        super().__init__(OrganizationService)

orgnization_controller = OrgnizationController()

urlpatterns = orgnization_controller.get_urls()

urlpatterns += [
    path('invite/<uuid:organization_id>/', OrganizationService.invite, name='user_organization_invite'),
#     path('join/<uuid:organization_id>/',OrganizationService.join, name='user_join_organization'),
#     path('leave/<uuid:organization_id>/',OrganizationService.leave, name='user_leave_organization'),
#     path('revoke-invite/<uuid:organization_id>/<uuid:user_id>/',OrganizationService.revoke_invite,name='revoke_invite')
]

for url in urlpatterns:
    print(url)