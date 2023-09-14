import { HttpClient, HttpParams } from '@angular/common/http';
import { AfterContentInit, Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Message } from '@app/models/chatMessage';
import { Classroom } from '@app/models/classroom';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Interaction } from '@app/models/interaction';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { otherQueryParams, QueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { TableHeader, TableHeaderType } from '@app/models/table';
import { Ue, UeEc } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils/parse-query-params';
import { SocketService } from '@app/socket.service';
import { environment } from '@environments/environment';
import { TranslateService } from '@ngx-translate/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { UtilsService } from '../../utils.service';
import { ClassroomService } from '../classroom/classroom.service';
import { CollegeYearService } from '../college-year/college-year.service';
import { EcService } from '../ec/ec.service';
import { HomeService } from '../home.service';
import { JourneyService } from '../journey/journey.service';
import { MentionService } from '../mention/mention.service';
import { UeService } from '../ue/ue.service';
import { NoteService } from './note.service';
import { User } from '@app/models';


const BASE_URL = environment.authApiURL;
const CODE = "note"

interface DataItem {
  name: string;
  age: number;
  street: string;
  building: string;
  number: number;
  companyAddress: string;
  companyName: string;
  gender: string;
}

@Component({
  selector: 'app-note',
  templateUrl: './note.component.html',
  styleUrls: ['./note.component.less']
})
export class NoteComponent implements OnInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  @ViewChild('isValidated', { static: true }) isValidated!: TemplateRef<any>;
  headers: TableHeader[] = [];
  headerSpan: TableHeader[] = [];
  headerData: TableHeader[] = [];



  listOfData: DataItem[] = [];
  sortAgeFn = (a: DataItem, b: DataItem): number => a.age - b.age;
  nameFilterFn = (list: string[], item: DataItem): boolean => list.some(name => item.name.indexOf(name) !== -1);

  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  allColumnUe: any[] = []
  allColumnEc: any[] = []
  allColumns: any[] = []
  allStudents: any[] = []
  listOfSemester?: string[] = []
  listOfSession = ["Normal", "Rattrapage", "Final"]
  listOfFilter = ["Moyenne", "Credit"]
  confirmModal?: NzModalRef
  form!: FormGroup;
  formDial!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  title = '';
  uuid = "";
  data = ""
  value = 10
  matierUe: Ue[] = [];
  matierEc: Ec[] = [];
  valueUe: string = ""
  isSpinning: boolean = false
  isVisible: boolean = false
  searchValue: string = ""
  result: string = ""
  message: string = ""
  initialise: boolean = false
  visibleDialog: boolean = false
  isResult: boolean = false
  isRattrape: boolean = false
  listOfDisplayData = [...this.allStudents]
  showStep: boolean = false
  showTable: boolean = false
  testMatier: boolean = false
  tableName: string = ""
  totalUe: number = 0
  totalEc: number = 0
  totalCredit: number = 0
  year: string = ""
  session: string = "Normal"
  interactionResult: Interaction[] = []
  disabled = true
  initialiseTemplate = false
  url_excel = "assets/images/face.png";
  msg!: string;
  url: string | ArrayBuffer | null = "";
  uploadedFile: any;
  user!: User
  disableCompense: boolean = true

  keyMention = CODE + "mention"
  keyYear = CODE + "collegeYear"
  keyNum: string | null = null
  keyJourney = CODE + "journey"
  keySemester = CODE + "semester"
  keySession = CODE + "session"
  keyUe: string | null = null
  keyEc: string | null = null
  keyType: string | null = null
  keyCredit: string | null = null
  keyValue: number | null = null
  keyMean: string | null = null
  isLoading: boolean = false
  permissionNote: boolean = false
  listRoom: Classroom[] = []

  actions = {
    add: true,
    edit: false,
    delete: false,
    detail: false,
  };

  matier: UeEc[] = []
  constructor(
    private http: HttpClient,
    private modal: NzModalService,
    private fb: FormBuilder,
    public authService: AuthService,
    private translate: TranslateService,
    private router: Router,
    private downloadServices: UtilsService,
    private serviceYear: CollegeYearService,
    private noteService: NoteService,
    private socketService: SocketService,
    private serviceRoom: ClassroomService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceUe: UeService,
    private serviceEc: EcService,) {

    this.form = this.fb.group({
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      session: [null, [Validators.required]],
      collegeYear: [null],
      matierUe: [null],
      matierEc: [null],
      semester: [null, [Validators.required]],
      meanCredit: [null],
      filter: [null],
      salle: [null, [Validators.required]],
      from: [null, [Validators.required]],
      to: [null, [Validators.required]],
    });
  }

  editCache: { [key: string]: { edit: boolean; data: any } } = {};
  current = 0;
  checked = false;
  indeterminate = false;
  index = 'First-content';
  listOfCurrentPageData: readonly Ue[] = [];
  setOfCheckedId = new Set<string>();
  expandSet = new Set<string>();
  interactionList: Interaction[] = []

  createHeaders() {
    this.headers = [
      {
        title: 'Validée',
        selector: 'validation',
        isSortable: false,
        rowspan: 2,
        template: this.isValidated,
        type: TableHeaderType.LEFT,
        width: "90px",
        style: { 'text-align': 'center' },
      },
      {
        title: "Num Carte",
        selector: "num_carte",
        isSortable: false,
        rowspan: 2,
        type: TableHeaderType.LEFT,
        width: "130px"
      }
    ]
    this.headerData = [
      {
        title: 'Validée',
        selector: 'validation',
        isSortable: false,
        rowspan: 2,
        width: "90px",
        template: this.isValidated,
        type: TableHeaderType.LEFT,
        style: { 'text-align': 'center' },
      },
      {
        title: "Num Carte",
        selector: "num_carte",
        isSortable: false,
        rowspan: 2,
        type: TableHeaderType.LEFT,
        width: "130px"
      }
    ]


    this.headerSpan = []
    for (let index = 0; index < this.allColumns.length; index++) {
      let column: TableHeader;
      column = {
        title: this.allColumns[index].title,
        selector: "ue_" + this.allColumns[index].name,
        isSortable: false,
        // width:`${100*this.allColumns[index].nbr_ec+ 90}`,
        colspan: this.allColumns[index].nbr_ec + 1,
      }
      this.headers.push(column)
      for (let j = 0; j < this.allColumns[index].nbr_ec; j++) {
        let column: TableHeader;
        column = {
          title: this.allColumns[index].ec[j].title,
          selector: "ec_" + this.allColumns[index].ec[j].name,
          isSortable: false,
          editable: true,
        }
        this.headerData.push(column)
        this.headerSpan.push(column)
      }

      this.headerData.push(
        {
          title: 'Note',
          selector: "ue_" + this.allColumns[index].name,
          isSortable: false,
          style: { 'text-align': 'center' },
        },
      )
      this.headerSpan.push(
        {
          title: 'Note',
          selector: "ue_" + this.allColumns[index].name,
          isSortable: false,
          width: "90px",
          style: { 'text-align': 'center' },
        },
      )

    }
    this.headers.push(
      {
        title: 'Credit',
        selector: 'credit',
        isSortable: false,
        rowspan: 2,
        width: "90px",
        style: { 'text-align': 'center' },
      },
    )
    this.headerData.push(
      {
        title: 'Credit',
        selector: 'credit',
        isSortable: false,
        width: "90px",
        style: { 'text-align': 'center' },
      },
    )
    this.headers.push(
      {
        title: 'Moyenne',
        selector: 'mean',
        isSortable: false,
        rowspan: 2,
        width: "90px",
        style: { 'text-align': 'center' },
      },
    )

    this.headerData.push(
      {
        title: 'Moyenne',
        selector: 'mean',
        width: "90px",
        isSortable: false,
        style: { 'text-align': 'center' },
      },
    )

    this.headers.push(
      {
        title: 'Action',
        selector: '',
        isSortable: false,
        type: TableHeaderType.ACTION,
        btnType: true,
        width: "90px",
        rowspan: 2,
      },
    )
    this.headerData.push(
      {
        title: 'Action',
        selector: '',
        isSortable: false,
        type: TableHeaderType.ACTION,
        btnType: true,
        width: "90px",
      },
    )
  }

  async ngOnInit() {
    // get College year
    let allYears: ResponseModel = await this.serviceYear.getDataPromise().toPromise()
    this.allYears = allYears.data

    // get all room
    let listRoom: ResponseModel = await this.serviceRoom.getDataPromisee().toPromise()
    this.listRoom = listRoom.data
    // get mention by permission
    this.user = await this.noteService.getMe().toPromise()
    if (!this.user.is_superuser) {
      this.allMention = await this.noteService.getMentionUser()
      if (this.testStorage(this.keyMention, this.allMention[0].uuid) &&
        this.testStorage(this.keyYear, this.allYears[0].title)) {
        let uuidMention = localStorage.getItem(this.keyMention)
        if (uuidMention !== null) {
          this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()
        }
        if (this.testStorage(this.keyJourney, this.allJourney[0].uuid)) {
          this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
          this.fetchData = this.fetchData.bind(this)
          if (
            this.testStorage(this.keySession, 'Normal') &&
            this.testStorage(this.keySemester, this.allJourney[0].semester[0])) {
            this.noteService.testNote(
              this.form.value.semester,
              this.form.value.journey,
              this.form.value.session
            ).subscribe(async () => {
              this.getNoteMatier()
              this.allColumns = await this.noteService.getAllColumns(
                this.form.value.semester,
                this.form.value.journey,
                this.form.value.session,
                this.form.value.collegeYear,
              ).toPromise()

              this.createHeaders()
              this.showTable = true
              this.isLoading = true
              this.fetchData = this.fetchData.bind(this)
              this.form.get('filter')?.setValue('Credit')

            },
              async () => {
                this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
                this.showTable = false
              }
            )
          }
        }
      }
      let permission = await this.noteService.getPermission(this.authService.userValue?.email, 'note').toPromise()
      if (permission) {
        this.permissionNote = permission.accepted
      }
      this.initialise = true
    } else {
      this.form.get('salle')?.clearValidators()
      this.form.get('from')?.clearValidators()
      this.form.get('to')?.clearValidators()

      let allMention: ResponseModel = await this.serviceMention.getDataPromise().toPromise()
      this.allMention = allMention.data

      if (this.testStorage(this.keyMention, this.allMention[0].uuid) &&
        this.testStorage(this.keyYear, this.allYears[0].title)) {
        let uuidMention = localStorage.getItem(this.keyMention)

        if (uuidMention !== null) {
          this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()
        }
        if (this.allJourney.length > 0) {
          if (this.testStorage(this.keyJourney, this.allJourney[0].uuid)) {
            this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
            // let testNote: boolean = await this.noteService.testNote(this.form.value.semester,
            //   this.form.value.journey,
            //   this.form.value.session).toPromise()

            this.testStorage(this.keySession, 'Normal')
            this.testStorage(this.keySemester, this.allJourney[0].semester[0])
            if (
              this.testStorage(this.keySession, 'Normal') &&
              this.testStorage(this.keySemester, this.allJourney[0].semester[0])) {
              this.noteService.testNote(
                this.form.value.semester,
                this.form.value.journey,
                this.form.value.session
              ).subscribe(async () => {
                this.getNoteMatier()
                this.allColumns = await this.noteService.getAllColumns(
                  this.form.value.semester,
                  this.form.value.journey,
                  this.form.value.session,
                  this.form.value.collegeYear,
                ).toPromise()

                this.createHeaders()
                this.showTable = true
                this.isLoading = true
                this.fetchData = this.fetchData.bind(this)
                this.form.get('filter')?.setValue('Credit')

              },
                async () => {
                  this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
                  this.showTable = false
                }
              )
            }
          }
        }
      }
      this.initialise = true
    }

  }


  testStorage(key: string, value: string): boolean {
    if (localStorage.getItem(key)) {
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    } else {
      localStorage.setItem(key, value)
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }
    return true
  }

  fetchData(params?: QueryParams) {
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      session: localStorage.getItem(this.keySession),
      semester: localStorage.getItem(this.keySemester),
      uuid_journey: localStorage.getItem(this.keyJourney),
      value_ue: this.keyUe,
      value_ec: this.keyEc,
      credit: this.keyCredit,
      mean: this.keyMean,
      value: this.keyValue,
      type_: this.keyType,
      num_carte: this.keyNum
    }
    return this.noteService.getDataObservable(parseQueryParams(params, otherParams))
  }

  onExpandChange(id: string, checked: boolean): void {
    if (checked) {
      this.expandSet.add(id);
    } else {
      this.expandSet.delete(id);
    }
  }

  resultUeSuccess(valueUe: string) {
    if (valueUe) {
      this.keyEc = null
      this.keyUe = valueUe
      this.keyType = "success"
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  resultUeFaild(valueUe: string) {
    if (valueUe) {
      this.keyEc = null
      this.keyUe = valueUe
      this.keyType = "failed"
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  resultEcSuccess(valueEc: string) {
    if (valueEc) {
      this.keyEc = valueEc
      this.keyUe = null
      this.keyType = "success"
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  resultEcFailed(valueEc: string) {
    if (valueEc) {
      this.keyEc = valueEc
      this.keyUe = null
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyType = "failed"
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  searchByNum(numCarte: any) {
    if (numCarte) {
      this.keyEc = null
      this.keyUe = null
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyType = null
      this.keyNum = numCarte
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  reset() {
    this.keyEc = null
    this.keyUe = null
    this.keyCredit = null
    this.keyValue = null
    this.keyMean = null
    this.keyType = null
    this.keyNum = null
    this.datatable.fetchData()
  }

  resultByCreditSuccess(data: any) {
    if (data) {
      this.keyEc = null
      this.keyUe = null
      this.keyCredit = data.credit
      this.keyValue = data.value
      this.keyMean = data.mean
      this.keyType = "success"
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  rattrapageList(data: any) {
    if (data) {
      this.keyEc = data.valueEc
      this.keyUe = data.valueUe
      this.keyType = null
      this.keyCredit = null
      this.keyValue = null
      this.keyMean = null
      this.keyNum = null
      this.datatable.fetchData()
    } else {
      this.reset()
    }
  }

  changeYear() {
    if (this.form.value.collegeYear && this.initialise) {
      localStorage.setItem(this.keyYear, this.form.value.collegeYear)
      this.refresh()
    }
  }
  updateCheckedSet(id: string, checked: boolean): void {
    if (checked) {
      this.setOfCheckedId.add(id);
    } else {
      this.setOfCheckedId.delete(id);
    }
  }
  onAllChecked(value: boolean): void {
    this.listOfCurrentPageData.forEach(item => this.updateCheckedSet(item.value, value));
    this.refreshCheckedStatus();
  }

  onItemChecked(id: string, checked: boolean): void {
    this.updateCheckedSet(id, checked);
    this.refreshCheckedStatus();
  }

  onCurrentPageDataChange($event: readonly Ue[]): void {
    this.listOfCurrentPageData = $event;
    this.refreshCheckedStatus();
  }

  refreshCheckedStatus(): void {
    this.checked = this.listOfCurrentPageData.every(item => this.setOfCheckedId.has(item.value));
    this.indeterminate = this.listOfCurrentPageData.some(item => this.setOfCheckedId.has(item.value)) && !this.checked;

  }

  demande() {
    let chatMsg: Message = { message: "demande de permission note" }
    this.socketService.sendMessage(chatMsg)
    this.socketService.createNotification("bottomRight", "Demande envoyé", "Demande")
  }

  pre(): void {
    this.current -= 1;
    this.totalEc = 0
    this.totalUe = 0
    this.totalCredit = 0
  }

  async next() {
    this.interactionList = []
    this.current += 1;
    if (this.current == 1) {
      const nameJourney = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
      this.tableName = this.form.value.semester + " " + nameJourney?.abbreviation
      this.year = this.form.value.collegeYear
      this.setOfCheckedId.forEach(item => this.getEc(item))
      let interaction: any = {}
      for (let index = 1; index <= 10; index++) {
        if ("S" + index === this.form.value.semester) {
          interaction["s" + index] = this.interactionList;
          break;
        }
      }
      interaction["uuid_journey"] = this.form.value.journey
      interaction["college_year"] = this.form.value.collegeYear

      let data = await this.noteService.addInteraction(this.form.value.semester, interaction).toPromise()

      for (let index = 0; index < data.length; index++) {
        this.interactionResult.push(data[index])
        if (data[index].type == "ue") {
          this.totalUe++
          this.totalCredit += data[index].value
        } else {
          this.totalEc++

        }
      }

    } else {
      if (this.interactionResult.length > 0) {
        await this.noteService.createTableNote(this.form.value.semester, this.form.value.journey, this.form.value.collegeYear).toPromise()
      }
    }

  }

  getEc(value_ue: string): void {
    const ue = this.matier.find((item: UeEc) => item.value === value_ue)
    if (ue) {
      this.interactionList.push({ name: ue?.value, title: ue?.title, value: ue?.credit, type: 'ue' })
      for (let index = 0; index < ue.ec.length; index++) {
        this.interactionList.push({ name: ue.ec[index].value, title: ue.ec[index].title, value: ue.ec[index].weight, type: 'ec' })
      }
    }

  }

  async done() {
    let testNote: boolean = await this.noteService.testNote(
      this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
    if (testNote) {
      this.submitForm()
      this.showTable = true
    }
  }

  getColumsType(str: string): string {
    return str.substring(0, 3)
  }

  getColumsName(str: string): string {
    return str.substring(3)
  }

  async createModel(note: any) {
    this.isSpinning = true
    let ue: any[] = []
    for (let i = 0; i < this.allColumns.length; i++) {
      let ueName = this.allColumns[i].name
      let ec: any[] = []
      for (let j = 0; j < this.allColumns[i].nbr_ec; j++) {
        let ecName = this.allColumns[i].ec[j].name
        let modelEc = { "name": ecName, "note": note["ec_" + this.allColumns[i].ec[j].name] }
        ec.push(modelEc)
      }
      let modelUe = { "name": ueName, "ec": ec }
      ue.push(modelUe)
    }
    let model = { "num_carte": note["num_carte"], "ue": ue }

    await this.noteService.insertNote(this.form.value.semester, this.form.value.journey,
      this.form.value.session, this.form.value.collegeYear, model).toPromise()
    this.datatable.fetchData()
    this.isSpinning = false
  }

  getTitle(data: any[], key: string, value: string): any {
    const name = data.find((item: any) => item[key] === value)
    return name
  }
  test(event: any) {
    console.error(event)
  }
  resultat(value_ue: string) {
    let url = `${BASE_URL}/resultat/get_by_matier_pdf`
    let params = new HttpParams()
      .append('college_year', this.form.value.collegeYear)
      .append('uuid_journey', this.form.value.journey)
      .append('semester', this.form.value.semester)
      .append('session', this.form.value.session)
      .append('value_ue', value_ue)

    const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
    let name = "resultat" + this.form.value.matierUe + "_" + this.form.get('semester')?.value + "_" + journey.abbreviation + "_" + this.form.value.session + '.pdf';
    this.downloadServices.download(url, params, name)

  }
  listExam() {
    let url = `${BASE_URL}/liste/list_exam/`
    let params = new HttpParams()
      .append('college_year', this.form.value.collegeYear)
      .append('uuid_journey', this.form.value.journey)
      .append('semester', this.form.value.semester)
      .append('session', this.form.value.session)
      .append('uuid_mention', this.form.value.mention)
      .append('salle', this.form.value.salle)
      .append('skip', this.form.value.from - 1)
      .append('limit', this.form.value.to)

    const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
    let name = "List_examen" + this.form.get('semester')?.value + "_" + journey.abbreviation + "salle"
    this.downloadServices.download(url, params, name)
    this.visibleDialog = false

  }

  onDelete(row: any) {
    this.showConfirmStudent(row)
  }

  onEdit(row: any) {
    this.createModel(row)
  }

  onAdd() {
    this.showModal();
  }
  compareNoteInfEc(): void {
    if (this.form.value.matierEc) {
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_" + this.form.value.matierEc] < 10);
      const name = this.matierEc.find((item: Ec) => item.value === this.form.value.matierEc)
      this.message = this.listOfDisplayData.length + " " +
        this.translate.instant('admin.home.note.message_ec_echec') + " " + name?.title
    } else {
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  setVisible(): void {
    this.isVisible = !this.isVisible
  }
  search(): void {
    this.listOfDisplayData = this.allStudents.filter((item: any) => item.name.indexOf(this.searchValue) !== -1);
  }
  async getStorage() {
    this.form.get('collegeYear')?.setValue(localStorage.getItem('collegeYear'))
    this.form.get('mention')?.setValue(localStorage.getItem('mention'))
    this.form.get('semester')?.setValue(localStorage.getItem('semester'))
    this.form.get('session')?.setValue(localStorage.getItem('session'))
    this.form.get('journey')?.setValue(localStorage.getItem('journey'))
    this.form.get('filter')?.setValue(localStorage.getItem('filter'))
  }


  showConfirmStudent(numCarte: string): void {
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer " + numCarte + "?",
      nzOnOk: async () => {
        await this.noteService.deleteNote(this.form.value.semester, this.form.value.journey, numCarte
          , this.form.value.session, this.form.value.collegeYear).toPromise()
        this.datatable.fetchData()
      }
    })
  }

  deleteTable(): void {
    if (this.form.get('journey')?.value && this.form.get('semester')?.value && this.form.get('session')?.value) {
      const journey = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
      this.confirmModal = this.modal.confirm({
        nzTitle: "Voulez-vous supprimer la table note " + this.form.get('semester')?.value + " " + journey?.abbreviation + " " + this.form.get('session')?.value + "?",
        nzOnOk: async () => {
          await this.noteService.deleteTable(this.form.value.semester, this.form.value.journey
            , this.form.value.session).toPromise()
        }
      })
    }
  }
  async createTable() {
    this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
    this.showTable = false
  }

  async insertStudent() {
    if (this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value && this.initialise) {
      await this.noteService.insertStudent(this.form.value.semester, this.form.value.journey,
        this.form.value.session, this.form.value.collegeYear, this.form.value.mention).toPromise()
      this.datatable.fetchData()
    }
  }

  async submitForm() {
    this.showStep = true
    this.form.get('salle')?.clearValidators()
    this.form.get('from')?.clearValidators()
    this.form.get('to')?.clearValidators()
    if (this.form.valid) {
      //this.datatable.fetchData()
      this.isvisible = false,
        this.isConfirmLoading = false
    } else {
      Object.values(this.form.controls).forEach(control => {
        if (control.invalid) {
          control.markAsDirty();
          control.updateValueAndValidity({ onlySelf: true });
        }
      });
    }
  }


  async getJourney() {
    if (this.form.get('mention')?.value) {
      this.form.get('journey')?.setValue('')
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.value.mention).toPromise()
    }
  }
  async changeJourney() {
    console.log(this.form.value.journey);

    if (this.form.value.journey) {
      localStorage.setItem(this.keyJourney, this.form.value.journey)
      this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
      this.refresh()
    }
  }
  async getAllColumnsSession() {

    if (this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('semester')?.value && this.initialise) {
      if (this.form.value.session == "Normal") {
        this.disableCompense = true
      } else {
        this.disableCompense = false
      }

      let testNote: boolean = await this.noteService.testNote(
        this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()

      localStorage.setItem(this.keySession, this.form.get('session')?.value)
      if (testNote) {
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
        this.createHeaders()
        this.datatable.fetchData()
      } else {
        this.matier = []
        this.showTable = false
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
      this.session = this.form.get('session')?.value
    }
  }

  async getNoteMatier() {
    this.matierEc = await this.serviceEc.getEc(this.form.value.semester, this.form.value.journey).toPromise()
    this.matierUe = await this.serviceUe.getUe(this.form.value.semester, this.form.value.journey).toPromise()
    let data = await this.noteService.getAllColumns(this.form.value.semester, this.form.value.journey,
      this.form.value.session, this.form.value.collegeYear).toPromise()
    this.allColumns = data
    this.allColumnUe = []
    this.allColumnEc = []
    for (let i = 0; i < data.length; i++) {
      const name = this.matierUe.find((item: Ue) => item.value === data[i]['name'])
      this.allColumnUe.push({ name: name?.title, value: data[i]['name'], nbr_ec: data[i]['nbr_ec'] })
      let ec = data[i]['ec']
      for (let j = 0; j < ec.length; j++) {
        const name = this.matierEc.find((item: Ec) => item.value === ec[j]['name'])
        this.allColumnEc.push({ name: name?.title, value: ec[j]['name'] })
      }
    }
    this.listOfDisplayData = [...this.allStudents]
    localStorage.setItem(this.keyJourney, this.form.get('journey')?.value)
    localStorage.setItem(this.keySemester, this.form.get('semester')?.value)
    localStorage.setItem(this.keySession, this.form.get('session')?.value)
    localStorage.setItem(this.keyMention, this.form.get('mention')?.value)

  }
  async refresh() {
    if (this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value && this.initialise) {
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      if (testNote) {
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
        this.createHeaders()
        this.datatable.fetchData()
      } else {
        this.matier = []
        this.showTable = false
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
    }
  }

  async getAllColumnsSemester() {
    if (this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.initialise) {
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      localStorage.setItem(this.keySemester, this.form.get('semester')?.value)
      if (testNote) {
        console.log(testNote);
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
        this.createHeaders()
        this.datatable.fetchData()
      } else {
        console.log("ato");

        this.matier = []
        this.showTable = false
        this.matier = await this.serviceUe.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
    } else {
      console.log("ato");

    }
  }


  async getAllJourney() {
    if (this.form.value.mention && this.isLoading) {
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.value.mention).toPromise()
    }
  }

  showModal(): void {
    this.visibleDialog = true;
  }

  handleCancel(): void {
    this.visibleDialog = false
  }

  viewNoteDetails(num: string): void {
    localStorage.setItem('numDetails', num)
    localStorage.setItem('collegeYear', this.form.value.collegeYear)
    localStorage.setItem('journey', this.form.value.journey)
    localStorage.setItem('semester', this.form.value.semester)
    localStorage.setItem('session', this.form.value.session)

    if (!this.user.is_superuser) {
      this.router.navigate(['/user/note-details']);
    }
    else {
      this.router.navigate(['/home/note-details'])
    }
  }
  async startUpload() {
    const formData = new FormData();
    if (this.url !== "" && this.initialise && this.form.value.semester && this.form.value.session && this.form.value.journey && this.form.value.collegeYear) {
      this.isConfirmLoading = true
      formData.append("uploaded_file", this.uploadedFile)
      let listOfData: ResponseModel = await this.noteService.uploadFile(formData, this.form.value.semester, this.form.value.session, this.form.value.journey, this.form.value.collegeYear).toPromise()
      this.listOfData = listOfData.data
      this.isConfirmLoading = false
      this.datatable.fetchData()
      this.isvisible = false
      this.visibleDialog = false
      this.initialiseTemplate = true
      this.uploadedFile = null
      this.disabled = true
    } else {
      console.log("Required parameters");

    }
  }
  startDownloadModel() {
    let url: string = `${BASE_URL}/save_data/get_models_notes/`;

    if (this.form.value.semester && this.form.value.session && this.form.value.journey && this.form.value.collegeYear) {
      let otherParams = new HttpParams().append('semester', this.form.value.semester)
        .append('session', this.form.value.session)
        .append('uuid_journey', this.form.value.journey)
        .append('college_year', this.form.value.collegeYear)
      let name: string = 'Model_note_' + this.form.value.semester + "_" + this.form.value.session
      this.downloadServices.download(url, otherParams, name, ".xlsx");
      this.visibleDialog = false
    }
  }

  startDownloadResultat(typeResult: string) {
    let url: string = `${BASE_URL}/resultat/get_by_session`;

    if (this.form.value.semester && this.form.value.session && this.form.value.journey && this.form.value.collegeYear) {
      let otherParams = new HttpParams().append('semester', this.form.value.semester)
        .append('session', this.form.value.session)
        .append('uuid_journey', this.form.value.journey)
        .append('college_year', this.form.value.collegeYear)
        .append('type_result', typeResult)
      let name: string = 'Resultat' + this.form.value.semester + "_" + this.form.value.session + "_" + typeResult
      this.downloadServices.download(url, otherParams, name);
      this.visibleDialog = false
    }
  }
  selectFile(event: any) {
    if (!event.target.files[0] || event.target.files[0].length == 0) {
      this.msg = "select a file"
      this.disabled = true
    } else {
      this.disabled = false
    }
    var mineType = event.target.files[0].type;
    if (mineType.match(/document\/*/) == null) {
      this.msg = "select image"
    }
    var reader = new FileReader();
    reader.readAsDataURL(event.target.files[0])

    reader.onload = (_event) => {
      this.msg = ""
      this.url = reader.result
    }
    this.uploadedFile = event.target.files[0]
    this.disabled = false
  }

}

