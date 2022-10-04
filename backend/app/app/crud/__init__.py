
from .crud_user import user
from .crud_mention import mention
from .crud_role import role
from .crud_journey import journey
from .crud_semester import semester
from .crud_college_years import college_year
from .crud_semester_valide import semester_valide
from .crud_ancien_etudiant import ancien_etudiant
from .crud_nouveau_etudiant import nouveau_etudiant
from .crud_matier_ue import matier_ue
from .crud_matier_ec import matier_ec
from .crud_note import note
from .crud_save import save
from .crud_diplome import diplome
from .crud_droit import droit
from .crud_student import new_student, ancien_student
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
