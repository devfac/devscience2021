import { HttpClient, HttpParams } from '@angular/common/http';
import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Interaction } from '@app/models/interaction';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { otherQueryParams, QueryParams } from '@app/models/query';
import { TableHeader, TableHeaderType } from '@app/models/table';
import { Ue, UeEc } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils/parse-query-params';
import { environment } from '@environments/environment';
import { TranslateService } from '@ngx-translate/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { UtilsService } from '../../utils.service';
import { HomeService } from '../home.service';
import { JourneyService } from '../journey/journey.service';
import { NoteService } from './note.service';


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
export class NoteComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
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
  listOfSession = ["Normal" ,"Rattrapage" ,"Final"]
  listOfFilter = ["Moyenne" ,"Credit"]
  confirmModal?: NzModalRef
  form!: FormGroup;
  formDial!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  title = '';
  uuid= "";
  data = ""
  value = 10
  matierUe: Ue[]=[];
  matierEc: Ec[]=[];
  valueUe: string = ""
  isSpinning: boolean = false
  isVisible: boolean = false
  searchValue: string = ""
  result: string  = ""
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
  year: string = ""
  session: string = "Normal"
  interactionResult: Interaction[] = []

  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numCarte"
  keyJourney = CODE+"journey"
  keySemester = CODE+"semester"
  keySession = CODE+"session"
  isLoading: boolean = false

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
    private service: HomeService,
    private noteService: NoteService,
    private serviceJourney: JourneyService, ) { 
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

  async ngAfterContentInit() {
   
  }

  createHeaders(){
    this.headers =[
      {
        title: "Num Carte",
        selector: "num_carte",
        isSortable: false,
        rowspan: 2,
        type: TableHeaderType.LEFT,
        width:"130px"
        }
    ] 
    this.headerData =[
      {
        title: "Num Carte",
        selector: "num_carte",
        isSortable: false,
        rowspan: 2,
        type: TableHeaderType.LEFT,
        width:"130px"
        }
    ] 
   
    this.headerSpan = []
    for (let index = 0; index<this.allColumns.length; index++){
      let name = this.matierUe.find((item:Ue) => item.value ===  this.allColumns[index].name)
      let column: TableHeader;
      if (name){
        column =  {
          title: name.title,
          selector: "ue_"+this.allColumns[index].name,
          isSortable: false,
          colspan: this.allColumns[index].nbr_ec + 1,
          }
      }else{
        column =  {
          title: "Title",
          selector: "ue_"+this.allColumns[index].name,
          isSortable: false,
          colspan: this.allColumns[index].nbr_ec + 1,
          }
      }
      this.headers.push(column)
      for (let j=0; j<this.allColumns[index].nbr_ec; j++){
            let name = this.matierEc.find((item:Ec) => item.value ===  this.allColumns[index].ec[j].name)
            let column: TableHeader;
            if (name){
              column =  {
                title: name.title,
                selector: "ec_"+this.allColumns[index].ec[j].name,
                isSortable: false,
                editable: true,
                }
            }else{
              column =  {
                title: "Title",
                selector: "ec_"+this.allColumns[index].ec[j].name,
                isSortable: false,
                editable: true,
                }
            }
           this.headerData.push(column)
           this.headerSpan.push(column)
      }

      this.headerData.push(
        {
          title: 'Note',
          selector: "ue_"+this.allColumns[index].name,
          isSortable: false,
          style: { 'text-align': 'center' },
        },
      )
      this.headerSpan.push(
        {
          title: 'Note',
          selector: "ue_"+this.allColumns[index].name,
          isSortable: false,
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
        style: { 'text-align': 'center' },
      },
    ) 
    this.headerData.push(
      {
        title: 'Credit',
        selector: 'credit',
        isSortable: false,
        style: { 'text-align': 'center' },
      },
    ) 
    this.headers.push(
      {
        title: 'Moyenne',
        selector: 'mean',
        isSortable: false,
        rowspan: 2,
        style: { 'text-align': 'center' },
      },
    ) 
    this.headerData.push(
      {
        title: 'Moyenne',
        selector: 'mean',
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
        rowspan: 2,
        style: { 'text-align': 'center' },
      },
    ) 
    this.headerData.push(
      {
        title: 'Action',
        selector: '',
        isSortable: false,
        type: TableHeaderType.ACTION,
        btnType: true,

        style: { 'text-align': 'center' },
      },
    ) 
  }

  async ngOnInit(){
    // get College year
    this.allYears = await this.service.getCollegeYear().toPromise()
    // get mention by permission
    if(this.authService.getPermission()){
      this.allMention = await this.noteService.getMentionUser()
      if(this.testStorage(this.keyMention, this.allMention[0].uuid) && 
        this.testStorage(this.keyYear, this.allYears[0].title)){
          let uuidMention = localStorage.getItem(this.keyMention)
          if(uuidMention !== null){
            this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()
          }
           if(this.testStorage(this.keyJourney, this.allJourney[0].uuid)){
              this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
              this.fetchData = this.fetchData.bind(this)
              if(
                this.testStorage(this.keySession,'Normal') &&
                this.testStorage(this.keySemester, this.allJourney[0].semester[0])){
                let testNote: boolean = await this.noteService.testNote(
                  this.form.value.semester, 
                  this.form.value.journey, 
                  this.form.value.session
                  ).toPromise()
                  if(testNote){
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
                    this.initialise = true
                    this.fetchData = this.fetchData.bind(this)
                    this.form.get('filter')?.setValue('Credit')
                  }else{
                      this.showTable = false
                  }
              }
           }
          }
    }else{
      this.form.get('salle')?.clearValidators()
      this.form.get('from')?.clearValidators()
      this.form.get('to')?.clearValidators()

      this.allMention = await this.service.getMentionAdmin().toPromise()

      if(this.testStorage(this.keyMention, this.allMention[0].uuid) && 
        this.testStorage(this.keyYear, this.allYears[0].title)){
        let uuidMention = localStorage.getItem(this.keyMention)
        if(uuidMention !== null){
          this.allJourney = await this.serviceJourney.getDataByMention(uuidMention).toPromise()}
         if(this.testStorage(this.keyJourney, this.allJourney[0].uuid)){
            this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
            let testNote: boolean = await this.noteService.testNote(this.form.value.semester,
               this.form.value.journey,
               this.form.value.session).toPromise()
               this.testStorage(this.keySession,'Normal')
               this.testStorage(this.keySemester, this.allJourney[0].semester[0])
               if(
                this.testStorage(this.keySession,'Normal') &&
                this.testStorage(this.keySemester, this.allJourney[0].semester[0])){
                let testNote: boolean = await this.noteService.testNote(
                  this.form.value.semester, 
                  this.form.value.journey, 
                  this.form.value.session
                  ).toPromise()
                  if(testNote){
                      this.getNoteMatier()
                      this.allColumns = await this.noteService.getAllColumns(
                      this.form.value.semester, 
                      this.form.value.journey, 
                      this.form.value.session,
                      this.form.value.collegeYear,
                    ).toPromise()
                    
                    this.createHeaders()
                    console.log(this.headerData)
                    console.log(this.headerSpan)
                    console.log(this.headers)
                    this.showTable = true
                    this.isLoading = true
                    this.initialise = true
                    this.fetchData = this.fetchData.bind(this)
                    this.form.get('filter')?.setValue('Credit')
                  }else{
                this.showTable = false
                this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
              }
         }
        }
      }
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
      session: localStorage.getItem(this.keySession),
      semester: localStorage.getItem(this.keySemester),
      uuid_journey: localStorage.getItem(this.keyJourney),
    }
    return this.noteService.getDataObservable(parseQueryParams(params,otherParams))
  }

  onExpandChange(id: string, checked: boolean): void {
    if (checked) {
      this.expandSet.add(id);
    } else {
      this.expandSet.delete(id);
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
    console.log(this.setOfCheckedId.size)
    
  }

  pre(): void {
    this.current -= 1;
  }

  async next() {
    this.interactionList = []
    this.current += 1;
    if (this.current == 1){
      const nameJourney = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
      this.tableName = this.form.value.semester+" "+nameJourney?.abbreviation
      this.year = this.form.value.collegeYear
      this.setOfCheckedId.forEach(item => this.getEc(item))
      let interaction: any = {}
      for (let index = 1; index<= 10; index++){
        if ("S"+index === this.form.value.semester) {
            interaction["s"+index] = this.interactionList;
            break;
        }
      }
      interaction["uuid_journey"] = this.form.value.journey
      interaction["college_year"] = this.form.value.collegeYear
  
      let data = await this.noteService.addInteraction(this.form.value.semester, interaction).toPromise()
      for (let index = 0; index< data.length; index++){
        this.interactionResult.push(data[index])
            if (data[index].type == "ue"){
              this.totalUe ++
            }else{
              this.totalEc ++
            }
      }
    }else{
      console.log(this.interactionResult)
      if(this.interactionResult.length > 0){
        this.submitForm()
      }
    }
    
  }

  getEc(value_ue: string): void{
    const ue = this.matier.find((item:UeEc) => item.value === value_ue)
    if (ue){
      this.interactionList.push({name:ue?.value, value:ue?.credit, type:'ue'})
      for (let index = 0; index<ue.ec.length ; index++){
        this.interactionList.push({name:ue.ec[index].value, value:ue.ec[index].weight, type:'ec'})
      }
    }

  }

  done(): void {
    this.showTable = true
    console.log('done');
  }

  getColumsType(str: string): string{
    return str.substring(0,3)
  }

  getColumsName(str: string): string{
    return str.substring(3)
  }

  async createModel(note:any){
    this.isSpinning = true
    let ue:any[] = []
    for(let i=0;i<this.allColumns.length;i++){
        let ueName = this.allColumns[i].name
        let ec:any[] = []
        for(let j=0;j<this.allColumns[i].nbr_ec;j++){
            let ecName = this.allColumns[i].ec[j].name
            let modelEc = {"name":ecName, "note":note["ec_"+this.allColumns[i].ec[j].name]}
            ec.push(modelEc)
        }
        let modelUe = {"name":ueName, "ec":ec}
        ue.push(modelUe)
      }
    let model = {"num_carte":note["num_carte"], "ue":ue}
    console.log(model)
    await this.noteService.insertNote(this.form.value.semester, this.form.value.journey, 
      this.form.value.session, this.form.value.collegeYear, model).toPromise()
      this.datatable.fetchData()
    this.isSpinning = false
  }

  getTitle(data: any[], key: string, value: string): any{
    const name = data.find((item: any) => item[key] === value)
    return name
  }
  test(event: any){
    console.error(event)
  }
  resultat(value_ue: string){
    let url = `${BASE_URL}/resultat/get_by_matier_pdf`
    let params = new HttpParams()
                .append('college_year', this.form.value.collegeYear)
                .append('uuid_journey', this.form.value.journey)
                .append('semester', this.form.value.semester)
                .append('session', this.form.value.session)
                .append('value_ue', value_ue)
    
    const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
    let name = "resultat"+this.form.value.matierUe+"_"+this.form.get('semester')?.value+"_"+journey.abbreviation+"_"+this.form.value.session+'.pdf';
    this.downloadServices.download(url, params, name)
    
  }
  listExam(){
    let url = `${BASE_URL}/liste/list_exam/`
    let params = new HttpParams()
                .append('college_year', this.form.value.collegeYear)
                .append('uuid_journey', this.form.value.journey)
                .append('semester', this.form.value.semester)
                .append('session', this.form.value.session)
                .append('uuid_mention', this.form.value.mention)
                .append('salle', this.form.value.salle)
                .append('skip', this.form.value.from)
                .append('limit', this.form.value.to)

    const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
    let name ="List_examen"+this.form.get('semester')?.value+"_"+journey.abbreviation+"salle"
    this.downloadServices.download(url, params, name)
    
  }

  onDelete(row: any) {
  }

  onEdit(row: any) {
    this.createModel(row)
    console.log(row)
  }

  onAdd() {
    this.showModal();
  }
  compareNoteInfEc(): void{
    if (this.form.value.matierEc){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] < 10);
      const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ec_echec')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  setVisible(): void{
    this.isVisible = !this.isVisible
  }
  search(): void {
    this.listOfDisplayData = this.allStudents.filter((item: any) => item.name.indexOf(this.searchValue) !== -1);
  }
  async getStorage(){
    console.log(this.listOfFilter.find((item: string) => item == localStorage.getItem('filter')))
    this.form.get('collegeYear')?.setValue(localStorage.getItem('collegeYear'))
    this.form.get('mention')?.setValue(localStorage.getItem('mention'))
    this.form.get('semester')?.setValue(localStorage.getItem('semester'))
    this.form.get('session')?.setValue(localStorage.getItem('session'))
    this.form.get('journey')?.setValue(localStorage.getItem('journey'))
    this.form.get('filter')?.setValue(localStorage.getItem('filter'))
  }


  showConfirmStudent(numCarte: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+numCarte+"?",
      nzOnOk: async () => {
       await this.noteService.deleteNote(this.form.value.semester, this.form.value.journey
       ,this.form.value.session,this.form.value.collegeYear, numCarte).toPromise()
      }
    })
  }
  
  deleteTable(): void{
    if(this.form.get('journey')?.value && this.form.get('semester')?.value && this.form.get('session')?.value){
      const journey = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
      this.confirmModal = this.modal.confirm({
        nzTitle: "Voulez-vous supprimer la table note "+this.form.get('semester')?.value+" "+journey?.abbreviation+" "+this.form.get('session')?.value+"?",
        nzOnOk:async () => {
          await this.noteService.deleteTable(this.form.value.semester, this.form.value.journey
          ,this.form.value.sessionr).toPromise()
        }
      })
    }
  }
  async createTable(){
    if(this.form.get('journey')?.value && this.form.get('semester')?.value && this.form.get('session')?.value){
      await this.noteService.createTable(this.form.value.semester, this.form.value.journey, this.form.value.collegeYear)
      .toPromise()
    }
  }

  async insertStudent(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value && this.initialise) {
       await this.noteService.insertStudent( this.form.value.semester, this.form.value.journey, 
        this.form.value.session, this.form.value.collegeYear, this.form.value.mention).toPromise()
        this.datatable.fetchData()
      }
  }

  async submitForm() {
    this.showStep = true
    if (this.form.valid) {
      this.datatable.fetchData()
        this.isvisible = false,
        this.isConfirmLoading = false
      } else {
        console.error("form not vali")
        Object.values(this.form.controls).forEach(control => {
          if (control.invalid) {
            control.markAsDirty();
            control.updateValueAndValidity({ onlySelf: true });
          }
        });
      }
  }


  async getJourney(){
    if(this.form.get('mention')?.value ){
      this.form.get('journey')?.setValue('')
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.value.mention).toPromise()
    }
  }
  async changeJourney(){
    if(this.form.value.journey ){
      localStorage.setItem(this.keyJourney, this.form.value.journey)
      this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester
      console.log(this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem(this.keyJourney))?.semester, 
      this.form.value.journey, this.allJourney)
    }
  }
  async getAllColumnsSession(){
    console.log(this.initialise)
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('semester')?.value && this.initialise){
      let testNote: boolean = await this.noteService.testNote( 
        this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
    localStorage.setItem(this.keySession, this.form.get('session')?.value)
        if(testNote){
          this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
          this.getNoteMatier()
          this.showTable = true
          this.createHeaders()
          this.datatable.fetchData()
        }else{
          this.matier = []
          this.showTable = false
          this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
      this.session = this.form.get('session')?.value
    }
  }

  async getNoteMatier(){
    this.matierEc = await this.service.getEc(this.form.value.semester, this.form.value.journey).toPromise()
    this.matierUe = await this.service.getUe(this.form.value.semester, this.form.value.journey).toPromise()
    let data = await this.noteService.getAllColumns(this.form.value.semester, this.form.value.journey,
       this.form.value.session, this.form.value.collegeYear).toPromise()
    this.allColumns = data
    this.allColumnUe = []
    this.allColumnEc = []
    for (let i=0; i<data.length; i++){
        const name = this.matierUe.find((item:Ue) => item.value ===  data[i]['name'])
        this.allColumnUe.push({name: name?.title, value: data[i]['name'], nbr_ec: data[i]['nbr_ec'] })
        let ec = data[i]['ec']
        for (let j=0; j<ec.length; j++){
          const name = this.matierEc.find((item:Ec) => item.value ===  ec[j]['name'])
          this.allColumnEc.push({name: name?.title, value: ec[j]['name'] })
        }
    }
    this.listOfDisplayData = [...this.allStudents]
    localStorage.setItem(this.keyJourney, this.form.get('journey')?.value)
    localStorage.setItem(this.keySemester, this.form.get('semester')?.value)
    localStorage.setItem(this.keySession, this.form.get('session')?.value)
    localStorage.setItem(this.keyMention, this.form.get('mention')?.value)
     
  }
  async refresh(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value && this.initialise){
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      if(testNote){
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
        this.createHeaders()
        this.datatable.fetchData()
      }else{
        this.matier = []
        this.showTable = false
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
    }
    }
  }

  async getAllColumnsSemester(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.initialise){
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      localStorage.setItem(this.keySemester, this.form.get('semester')?.value)
      if(testNote){
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
        this.createHeaders()
        this.datatable.fetchData()
      }else{
        this.matier = []
        this.showTable = false
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
    }
    }
  }


 async getAllJourney(){
    if(this.form.value.mention && this.isLoading){
      this.allJourney = await this.serviceJourney.getDataByMention(this.form.value.mention).toPromise()
    }
  }

  showModal(): void{
    this.visibleDialog = true;
  }

  handleCancel(): void{
    this.visibleDialog = false
  }

  viewNoteDetails(num: string): void{
    localStorage.setItem('numDetails', num)
    localStorage.setItem('collegeYear', this.form.value.collegeYear)
    localStorage.setItem('journey', this.form.value.journey)
    localStorage.setItem('semester', this.form.value.semester)
    this.router.navigate(['/user/note-details'])
}

}

