# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.user import User  # noqa
from app.models.mention import Mention # noqa
from app.models.role import Role # noqa
from app.models.parcours import Parcours # noqa
from app.models.semestre import Semestre # noqa
from app.models.anne_univ import AnneUniv # noqa
