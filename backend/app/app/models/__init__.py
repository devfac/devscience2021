from sqlalchemy.sql.operators import is_natural_self_precedent
from .user import User
from .mention import Mention
from .role import Role
from .parcours import Parcours
from .semestre import Semestre
from .anne_univ import AnneUniv
from .etudiant import create
from .matier import create
from .note import create_table_note
from .droit import Droit