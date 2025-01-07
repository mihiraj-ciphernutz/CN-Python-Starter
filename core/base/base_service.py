from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

class BaseService:
    def __init__(self, database_class):
        self.database_class = database_class

    @csrf_exempt
    def list_items(self, request):
        """
        List all items from the database, with authentication check.
        """
        try:
            items = self.database_class().get_all()  
            if not items:                                          
                return JsonResponse({"message": "Items not found."}, status=404)
            return JsonResponse(items, safe=False)  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @csrf_exempt
    def get_item(self, request, id):
        """
        Retrieve a model instance by its ID using the database handler, with authentication check.
        """
        try:
            item = self.database_class().get_id(id)  
            return JsonResponse(model_to_dict(item))
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"Item with id {id} does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    @csrf_exempt
    def create_item(self, request):
        """
        Create a new model instance in the database, ensuring all required fields are provided, with authentication check.
        """
        try:
            data = json.loads(request.body)

            model = self.database_class().model

            for field in model._meta.get_fields():
                if hasattr(field, "unique") and field.unique:
                    field_value = data.get(field.name)
                    if field_value and model.objects.filter(**{field.name: field_value}).exists():
                        return JsonResponse(
                            {"error": "Item already exists."},
                            status=400
                        )

            created_item = self.database_class().create(**data)

            return JsonResponse({
                "message": "Item created successfully.",
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    @csrf_exempt
    def update_item(self, request, id):
        """
        Update an existing model instance by its ID, with authentication check.
        """
        try:
            data = json.loads(request.body) 
            updated_data = {}

            for field in data:
                updated_data[field] = data[field] 

            updated_item = self.database_class().update(id, **updated_data)  
            return JsonResponse({"message": f"Item updated successfully.",
                                 "updated_item" : model_to_dict(updated_item)}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"Item with id {id} does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete_item(self, request, id):
        """
        Delete a model instance by its ID, with authentication check.
        """
        try:
            self.database_class().delete(id)  
            return JsonResponse({"message": f"Item with id {id} deleted successfully."})
        except ObjectDoesNotExist:
            return JsonResponse({"error": f"Item with id {id} does not exist."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
