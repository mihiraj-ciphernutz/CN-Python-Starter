from core.base.base_service import BaseService
from core.organization.organization_database import OrganizationDatabase
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from core.models import Role, UserOrganizationRole, CustomUser, Organization
import json

class OrganizationService(BaseService):
    def __init__(self):
        super().__init__(OrganizationDatabase)

    def invite(request, organization_id):
        try:
            organization = get_object_or_404(Organization, id=organization_id)
            data = json.loads(request.body)
            user_id = data.get("user_id")
            role_id = data.get("role_id")

            if not user_id or not role_id:
                return JsonResponse({"error": "User ID and Role ID are required."}, status=400)

            user = get_object_or_404(CustomUser, id=user_id)
            role = get_object_or_404(Role, id=role_id)

            user_org_role = UserOrganizationRole.objects.create(
                customuser=user,
                organization=organization,
                role=role
            )

            return JsonResponse({"message": f"User {user.username} invited to organization {organization.name} as {role.name}."}, status=201)

        except Organization.DoesNotExist:
            return JsonResponse({"error": "Organization not found."}, status=404)
        except Role.DoesNotExist:
            return JsonResponse({"error": "Role not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # def join():
    #     pass

    # def leave():
    #     pass

    # def revoke_invite():
    #     pass