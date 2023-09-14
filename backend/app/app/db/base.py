# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.mention import Mention # noqa
from app.models.role import Role # noqa
from app.models.journey import Journey # noqa
from app.models.semester import Semester # noqa
from app.models.college_year import CollegeYear # noqa
from app.models.student import Student # noqa
from app.models.validation import Validation # noqa
from app.models.permission import Permission # noqa
from app.models.interaction import Interaction # noqa
from app.models.invitation import Invitation # noqa
from app.models.matier import ConstituentElement, TeachingUnit # noqa
from app.models.classroom import Classroom # noqa
from app.models.droit import Droit # noqa
from app.models.historic import Historic # noqa
