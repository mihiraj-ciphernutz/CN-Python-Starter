class BaseDatabase:
    model = None  

    def __init__(self, model=None):
        if model:
            self.model = model

    def get_all(self):
        """
        Get all objects from the database for the model.
        Should be overridden or used as is in child classes.
        """
        if not self.model:
            raise ValueError("Model is not defined.")
        return list(self.model.objects.all().values())

    def get_id(self, id):
        """
        Get a single model instance by its ID.
        """
        if not self.model:
            raise ValueError("Model is not defined.")
        return self.model.objects.get(id=id)
    
    def create(self, **data):
        """
        Create a new model instance.
        """
        if not self.model:
            raise ValueError("Model is not defined.")
        return self.model.objects.create(**data)

    def update(self, id, **data):
        """
        Update an existing model instance by its ID.
        """
        if not self.model:
            raise ValueError("Model is not defined.")
        obj = self.model.objects.get(id=id)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, id):
        """
        Delete a model instance by its ID.
        """
        if not self.model:
            raise ValueError("Model is not defined.")
        obj = self.model.objects.get(id=id)
        obj.delete()
        return obj
    
    def filter(self, **kwargs):
        """
        Filters instances of the model class based on the given keyword arguments.
        """
        return self.model.objects.filter(**kwargs)