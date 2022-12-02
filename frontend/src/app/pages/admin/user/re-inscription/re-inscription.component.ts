import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams, otherQueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { AncienStudent, StudentColumn, ColumnItem } from '@app/models/student';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import {AuthService} from '../../../../services/auth/auth.service'
import { DownloadService } from '../../download.service';
import { CollegeYearService } from '../../home/college-year/college-year.service';
import { JourneyService } from '../../home/journey/journey.service';
import { MentionService } from '../../home/mention/mention.service';
import { UtilsService } from '../../utils.service';
import { ReInscriptionService } from './re-inscription.service';

const CODE = "reinscription"
const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-re-inscription',
  templateUrl: './re-inscription.component.html',
  styleUrls: ['./re-inscription.component.less']
})
export class ReInscriptionComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  allStudents: AncienStudent[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  formList!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  listOfData: any[] = []
  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numCarte"
  isEdit = false;
  title = '';
  data = ""
  uuid= "";
  url_face:any ="assets/images/face.png";
  url_pile:any ="assets/images/pile.png";
  isLoading: boolean = false

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
    print: true,
  };
  
  listOfColumns: ColumnItem[] = [

    {
      name:"Num carte",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Nom",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.last_name.localeCompare(b.last_name),
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },

    {
      name:"Prenom",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Semester inf",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.inf_semester.localeCompare(b.inf_semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: StudentColumn) => item.inf_semester.indexOf(semester) !== -1
    },
    {
      name:"Semester sup",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.sup_semester.localeCompare(b.sup_semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: StudentColumn) => item.sup_semester.indexOf(semester) !== -1
    },
    {
      name:"Parcours",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.journey.abbreviation.localeCompare(b.journey.abbreviation),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: [],
      filterFn:(list: string[], item: StudentColumn) => list.some(journey => item.journey.abbreviation.indexOf(journey) !== -1)
    },
    {
      name:"Action",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn:null
    },
  ]

  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public router: Router, 
    private authUser: AuthService, 
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: ReInscriptionService,
    private utlisService: UtilsService) { 


    this.form = this.fb.group({
      email: [null, [Validators.required]],
      firstName: [null, [Validators.required]],
      lastName: [null, [Validators.required]],
      isAdmin: [false],
      collegeYear: [null],
      uuidRole: [null, [Validators.required]],
      mention: [[], [Validators.required]],
      filter: [null],
    });
    this.formList = this.fb.group({
      semester: [null, [Validators.required]],
      journey: [null, [Validators.required]]
    })
  }

  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Num Carte',
      selector: 'num_carte',
      width: "100px",
      isSortable: true,
    },{
      title: 'Nom',
      selector: 'last_name',
      width:"250px",
      isSortable: true,
    },{
      title: 'Prenom',
      selector: 'first_name',
      width: "150px",
      isSortable: true,
    },{
      title: 'Semestre Inf.',
      selector: 'inf_semester',
      width: "100px",
      isSortable: true,
    },{
      title: 'Semestre sup.',
      selector: 'sup_semester',
      width: "100px",
      isSortable: true,
    },{
      title: 'Parcours',
      selector: 'journey.abbreviation',
      width: "100px",
      isSortable: true,
    },
  ];
  }

  async ngOnInit(){
    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let mention = await this.serviceMention.getData(user?.uuid_mention[i]).toPromise()
      this.allMention.push(mention)
          
    }

    
    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }
    let allYears: ResponseModel = await this.serviceYears.getDataPromise().toPromise()
    this.allYears = allYears.data
    
    
    if(this.testStorage(this.keyMention, this.allMention[0].uuid) && 
    this.testStorage(this.keyYear, this.allYears[0].title)){
      let uuidMention = localStorage.getItem(this.keyMention)
      if(uuidMention !== null){
        this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()}
        this.fetchData = this.fetchData.bind(this)
        this.isLoading = true
    }
  }
  testStorage(key: string, value: string): boolean{
    if(localStorage.getItem(key)){
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key.substring(CODE.length))?.setValue(localStorage.getItem(key))
    }
    return true
  }

  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      uuid_mention: localStorage.getItem(this.keyMention),
    }
    return this.service.getDataObservable(parseQueryParams(params,otherParams))
  }

  showConfirm(name: string, numCarte: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: async () => {
        await this.service.deletData(numCarte)
        this.datatable.fetchData()
      }
    })
  }
  
  showModalEdit(numCarte: string): void{
    this.isEdit = true
    localStorage.setItem(this.keyNum, numCarte)
    localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
    localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
    this.router.navigate(['/user/reinscription_add'])
  }


  onDelete(row: any) {
    this.showConfirm(row.title, row.uuid);
  }

  onEdit(row: any) {
    this.showModalEdit(row.num_carte);
  }

  onAdd() {
    this.addStudent();
  }
  
  handleCancel(): void{
    this.isvisible = false
  }

  getAllStudents(): void{
    if(this.form.get(this.keyYear.substring(CODE.length))?.value && 
    this.form.get(this.keyMention.substring(CODE.length))?.value && this.isLoading){
      localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
      localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
      this.datatable.fetchData()
    }
  }

  addStudent():void{
    localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
    localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
    this.router.navigate(['/user/reinscription_add'])
    localStorage.setItem(this.keyNum, '')
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }

  changeJourney(): void{
    if(this.formList.value.journey ){
      localStorage.setItem('journey', this.formList.value.journey)

      const journey = this.allJourney.find((item: Journey) => item.uuid === this.formList.value.journey)
      if (journey){
      this.listOfSemester = journey.semester
    }
    }
  }
  changeFilter(){
    if(this.form.value.filter){
      this.listOfData = this.allStudents.filter((item: any) => item.journey.uuid === this.form.value.filter)
    }else{
      this.listOfData = this.allStudents
    }
  }

  async showModal(){
    this.isEdit = false;
    this.isvisible = true;
    let mention = localStorage.getItem(this.keyMention)
    if (mention){
      this.allJourney = await this.serviceJourney.getDataByMention(mention).toPromise()}
  }
  startDownload(){
    let url: string = `${BASE_URL}/liste/list_inscrit/`;

    let params = new HttpParams()
      .append('college_year', this.form.get('collegeYear')?.value)
      .append('uuid_journey', this.formList.get('journey')?.value)
      .append('semester', this.formList.get('semester')?.value);

    const journey = this.allJourney.find((item: Journey) => item.uuid === this.formList.value.journey);
    let name: string = 'list_etudiants'+journey?.abbreviation+'_'+this.formList.get('semester')?.value;
    this.utlisService.download(url, params, name);
    this.isvisible = false;
  }

  startDownloadFace(){
    let url: string = `${BASE_URL}/carte/carte_student/`;

    let params = new HttpParams()
      .append('college_year', this.form.get('collegeYear')?.value)
      .append('uuid_mention', this.form.get('mention')?.value)

    const mention = this.allMention.find((item: Mention) => item.uuid === this.form.value.mention);
    let name: string = 'Face_carte'+mention?.abbreviation
    this.utlisService.download(url, params, name);
    this.isvisible = false;
  }

  startDownloadPile(){
    let url: string = `${BASE_URL}/carte/carte_after/`;

    let params = new HttpParams()
      .append('college_year', this.form.get('collegeYear')?.value)
      .append('uuid_mention', this.form.get('mention')?.value)

    const mention = this.allMention.find((item: Mention) => item.uuid === this.form.value.mention);
    let name: string = 'Arriere_carte'+mention?.abbreviation;
    this.utlisService.download(url, params, name);
    this.isvisible = false;
  }

  startDownloadPassant(){
    let url: string = `${BASE_URL}/liste/list_bourse_passant/`;

    let params = new HttpParams()
      .append('college_year', this.form.get('collegeYear')?.value)
      .append('uuid_mention', this.form.get('mention')?.value)

    const mention = this.allMention.find((item: Mention) => item.uuid === this.form.value.mention);
    let name: string = 'Bourse_Passant'+mention?.abbreviation
    this.utlisService.download(url, params, name);
    this.isvisible = false;
  }

  startDownloadRedoublant(){
    let url: string = `${BASE_URL}/liste/list_bourse_redoublant/`;

    let params = new HttpParams()
      .append('college_year', this.form.get('collegeYear')?.value)
      .append('uuid_mention', this.form.get('mention')?.value)

    const mention = this.allMention.find((item: Mention) => item.uuid === this.form.value.mention);
    let name: string = 'Bourse_Rédoublant'+mention?.abbreviation
    this.utlisService.download(url, params, name);
    this.isvisible = false;
  }

  download(){
    this.showModal()
  }
}
