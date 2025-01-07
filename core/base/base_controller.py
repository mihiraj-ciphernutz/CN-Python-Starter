from django.urls import path

class BaseController:
    """
    BaseController defines URLs by mapping to methods already present in the service.
    """

    def __init__(self, service_class):
        """
        Initialize with a service class containing the CRUD logic.
        """
        if not service_class:
            raise ValueError("service_class must be provided.")
        self.service_class = service_class()  

    def get_urls(self):
        """
        Generate URLs by mapping to the service methods.
        """
        model_name = self.service_class.__class__.__name__.replace('Service', '').lower()

        return [
            path('list/', self.service_class.list_items, name=f'{model_name}_list_items'),
            path('create/', self.service_class.create_item, name=f'{model_name}_create_item'),
            path('get/<uuid:id>/', self.service_class.get_item, name=f'{model_name}_get_item'),
            path('update/<uuid:id>/', self.service_class.update_item, name=f'{model_name}_update_item'),
            path('delete/<uuid:id>/', self.service_class.delete_item, name=f'{model_name}_delete_item'),
        ]