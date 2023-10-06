
from .crud_user import user
from .crud_mention import mention
from .crud_role import role
from .crud_journey import journey
from .crud_college_years import college_year
from .crud_matier import teaching_unit, constituent_element
from .crud_note import note
from .crud_save import save
from .crud_diploma import diploma
from .crud_enrollment_fee import enrollment_fee
from .crud_student import new_student, ancien_student
from .crud_interaction import interaction
from .crud_permission import permission
from .crud_invitation import invitation
from .crud_classroom import classroom
from .crud_bacc_serie import bacc_serie
from .crud_historic import historic
from .crud_validation import validation
from .crud_subscription import subscription
from .crud_user_mention import user_mention
from .crud_journey_semester import journey_semester
from .crud_student_years import student_years
from .crud_receipt import receipt
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
