from re import I
from .msg import Msg
from .token import Token, TokenPayload
from .user import User, UserCreate, UserInDB, UserUpdate, UserLogin
from .mention import Mention, MentionCreate, MentionInDB, MentionUpdate
from .role import Role, RoleCreate, RoleInDB, RoleUpdate
from .journey import Journey, JourneyCreate, JourneyInDB, JourneyUpdate
from .semester import Semester, SemesterCreate, SemesterInDB, SemesterUpdate
from .college_year import CollegeYearCreate, CollegeYear, CollegeYearUpdate, CollegeYearInDB
from .validation import  ValidationUpdate
from .etudiant import EtudiantAncien, EtudiantAncienCreate,EtudiantAncienUpdate,EtudiantAncienInDB, keys,EtudiantCarte
from .etudiant import EtudiantNouveau, EtudiantNouveauCreate, EtudiantNouveauUpdate, EtudiantNouveauInDB, SelectEtudiantBase
from .matier import MatierEC, MatierECCreate, MatierECInDB, MatierECUpdate
from .matier import MatierUE, MatierUECreate, MatierUEInDB, MatierUEUpdate, MatierUEEC
from .matier import MatierUni
from .note import Note, NoteUE
from .resultat import Resultat
from .diploma import Diploma, DiplomaCreate, DiplomaUpdate, DiplomaInDB
from .droit import Droit, DroitUpdate, DroitCreate, DroitInDB
from .student import AncienStudentCreate, AncienStudentUpdate, AncienStudent, AncienStudentInDB, CarteStudent, StudentUpdatePhoto
from .student import NewStudent, NewStudentCreate, NewStudentUpdate, NewStudentInDB, SelectStudentBase, SelectStudentCreate, NewStudentUploaded
from .interaction import InteractionInDBBase, InteractionUpdate, Interaction, InteractionInDB,  InteractionCreate, ValueUEEC
from .socket import SocketModel
from .permission import Permission, PermissionCreate, PermissionUpdate, PermissionCreateModel
from .invitation import Invitation, InvitationCreate, InvitationUpdate
from .classroom import Classroom, ClassroomCreate, ClassroomUpdate
from .response import ResponseData
from .bacc_serie import BaccSerieCreate, BaccSerieUpdate, BaccSerie
from .historic import Historic, HistoricCreate
from .publication import PublicationCreate, ShowPublication, PublicationUpdate
