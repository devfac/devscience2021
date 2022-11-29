
from .crud_user import user
from .crud_mention import mention
from .crud_role import role
from .crud_journey import journey
from .crud_semester import semester
from .crud_college_years import college_year
from .crud_validation import validation
from .crud_matier import teaching_unit, constituent_element
from .crud_note import note
from .crud_save import save
from .crud_diploma import diploma
from .crud_droit import droit
from .crud_student import new_student, ancien_student
from .crud_interaction import interaction
from .crud_permission import permission
from .crud_invitation import invitation
from .crud_classroom import classroom
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
