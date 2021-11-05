from .crud_user import admin, user, employee, patient, reporting_physician
from .study import study
from .crud_referring_physician import referring_physician
from .crud_type_study import type_study
from .crud_user_role import user_role
from .crud_role import role

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)