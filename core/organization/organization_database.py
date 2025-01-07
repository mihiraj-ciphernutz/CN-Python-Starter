import setup_django
from core.base.base_database import BaseDatabase
from core.models import Organization

class OrganizationDatabase(BaseDatabase):
    def __init__(self):
        super().__init__(Organization)
