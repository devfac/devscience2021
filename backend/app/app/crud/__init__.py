
from .crud_user import user
from .crud_mention import mention
from .crud_role import role
from .crud_parcours import parcours
from .crud_semestre import semetre
from .crud_anne_univ import anne_univ
from .crud_semestre_valide import semetre_valide
from .crud_ancien_etudiant import ancien_etudiant
from .crud_nouveau_etudiant import nouveau_etudiant
from .crud_matier_ue import matier_ue
from .crud_matier_ec import matier_ec
from .crud_note import note
from .crud_save import save
# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
