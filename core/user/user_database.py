import setup_django
from core.base.base_database import BaseDatabase
from core.models import CustomUser

class UserDatabase(BaseDatabase):
    def __init__(self):
        super().__init__(CustomUser)
