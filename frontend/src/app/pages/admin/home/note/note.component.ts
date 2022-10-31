import { HttpHeaders, HttpClient } from '@angular/common/http';
import { FactoryTarget } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Interaction } from '@app/models/interaction';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Ue, UeEc } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { TranslateService } from '@ngx-translate/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { DownloadService } from '../../download.service';
import { HomeService } from '../home.service';
import { NoteService } from './note.service';


const BASE_URL = environment.authApiURL;

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


  listOfData: DataItem[] = [];
  sortAgeFn = (a: DataItem, b: DataItem): number => a.age - b.age;
  nameFilterFn = (list: string[], item: DataItem): boolean => list.some(name => item.name.indexOf(name) !== -1);
  filterName = [
    { text: 'Joe', value: 'Joe' },
    { text: 'John', value: 'John' }
  ];
  column1 = [{name: 'Other', span: 4}, {name: 'Company', span: 2}]
  column2 = [
    "Age",
    "Address",
    "Building",
    "Door No.",
    "Company name",
    "Company Address"
  ]
  test1 = false
  


  
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

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
  interactionResult: Interaction[] = []

  options = {
    headers: this.headers
  }
  matier: UeEc[] = []
  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public authService: AuthService, 
    private translate: TranslateService,
    private router: Router,
    private downloads: DownloadService,
    private service: HomeService,
    private noteService: NoteService ) { 
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

  next(): void {
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
  
      this.http.post<Interaction[]>(`${BASE_URL}/interaction/?semester=`
      +this.form.get('semester')?.value, interaction ,this.options).subscribe(
        data => {
          for (let index = 0; index< data.length; index++){
            this.interactionResult.push(data[index])
                if (data[index].type == "ue"){
                  this.totalUe ++
                }else{
                  this.totalEc ++
                }
          }
        },
        error => console.error("error as ", error)
      );
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

  startEdit(id: string): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: string): void {
    const index = this.listOfDisplayData.findIndex(item => item.num_carte === id);
    this.editCache[id] = {
      data: { ...this.listOfDisplayData[index] },
      edit: false
    };
  }

  saveEdit(id: string): void {
    const index = this.listOfDisplayData.findIndex(item => item.num_carte === id);
    this.createModel(this.listOfDisplayData[index], index)
    this.editCache[id].edit = false;
  }

  getColumsType(str: string): string{
    return str.substring(0,3)
  }

  getColumsName(str: string): string{
    return str.substring(3)
  }



  createModel(note:any, index:number): void{
    this.isSpinning = true
    let ue:any[] = []
    for(let i=0;i<this.allColumns.length;i++){
      console.log(this.allColumns[i].value)
      if(this.getColumsType(this.allColumns[i].value) === 'ue_'){
        let ueName = this.getColumsName(this.allColumns[i].value)
        let ec:any[] = []
        for(let j=i+1;j<this.allColumns.length;j++){
          if(this.getColumsType(this.allColumns[j].value) === 'ec_'){
            let ecName = this.getColumsName(this.allColumns[j].value)
            let modelEc = {"name":ecName, "note":note[this.allColumns[j].value]}
            ec.push(modelEc)
          }else{
            break;
          }
        }
        let modelUe = {"name":ueName, "ec":ec}
        ue.push(modelUe)
      }
    }
    let model = {"num_carte":note["num_carte"], "ue":ue}
    console.log(model)
    this.http.post<any>(`${BASE_URL}/notes/insert_note?college_year=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, model ,this.options).subscribe(
          data => {
            this.isSpinning = false,
            //this.listOfDisplayData = [...this.allStudents]
            Object.assign(this.listOfDisplayData[index], data);
          },
          error => console.error("error as ", error)
        );
  }
  updateEditCache(): void {
    this.listOfDisplayData.forEach(item => {
      this.editCache[item.num_carte] = {
        edit: false,
        data: item
      };
    });
  }

  compareNoteSupUe(): void{
    if (this.form.value.matierUe){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ue_"+this.form.value.matierUe] >= 10);
      const name = this.matierUe.find((item:Ue) => item.value === this.form.value.matierUe)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ue_admis')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  compareNoteSupEc(): void{
    if (this.form.value.matierEc){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] >= 10);
      const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ec_admis')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  resetTableUe(): void{
    if (this.form.value.matierUe){
      this.result = this.form.value.matierUe
      this.isResult = true
    }else{
      this.listOfDisplayData = this.allStudents;
      this.isResult = false
    }
  }

  resetTableEc(): void{
    if (this.form.value.matierEc){
      this.result = this.form.value.matierEc
      this.isRattrape = true
    }else{
      this.listOfDisplayData = this.allStudents;
      this.isRattrape = false
    }
  }
  getTitle(data: any[], key: string, value: string): any{
    const name = data.find((item: any) => item[key] === value)
    return name
  }

  rattrapageList(): void{
    if (this.form.value.matierEc && this.form.value.session === 'Normal'){
        const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
        this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] < 10 && item["ue_"+name?.value_ue] < 10 )
        this.message = this.listOfDisplayData.length+" "+
        this.translate.instant('admin.home.note.message_ec_refaire')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  changeFilter(){
    if (this.form.value.filter){
      localStorage.setItem('filter', this.form.value.filter)
    }else{
      localStorage.setItem('filter', '')
    }
  }

  filterSup(): void{
    this.message = ""
    if (this.form.value.filter){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'sup')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['mean']  >= Number(value) )
        }else{
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['credit']  >= Number(value) )
        }
    }else{
      this.listOfDisplayData = this.allStudents
    }
  }

  filterInf(): void{
    this.message = ""
    if (localStorage.getItem('filter')){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'inf')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['mean']  < Number(value) )
        }else{
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['credit']  < Number(value) )
        }
    }else{
      this.listOfDisplayData = this.allStudents
    }
  }

  compareNoteInfUe(): void{
    if (this.form.value.matierUe){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ue_"+this.form.value.matierUe] < 10);
      const name = this.matierUe.find((item:Ue) => item.value === this.form.value.matierUe)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ue_echec')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }
  test(event: any){
    console.error(event)
  }

  resultat(): void{
    const url: string = `${BASE_URL}/resultat/get_by_matier_pdf?schema=`
    +this.form.get('collegeYear')?.value+`&uuid_journey=`
    +this.form.get('journey')?.value+`&semester=`
    +this.form.get('semester')?.value+`&session=`
    +this.form.get('session')?.value+`&value_ue=`
    +this.form.get('matierUe')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
        a.download = "resultat"+this.form.value.matierUe+"_"+this.form.get('semester')?.value+"_"+journey.abbreviation+"_"+this.form.value.session+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }

  listExam(): void{
    const url: string = `${BASE_URL}/liste/list_exam/?college_year=`
    +this.form.get('collegeYear')?.value+`&uuid_journey=`
    +this.form.get('journey')?.value+`&semester=`
    +this.form.get('semester')?.value+`&session=`
    +this.form.get('session')?.value+`&uuid_mention=`
    +this.form.get('mention')?.value+'&salle='
    +this.form.get('salle')?.value+'&skip='
    +this.form.get('from')?.value+'&limit='
    +this.form.get('to')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
        a.download ="List_examen"+this.form.get('semester')?.value+"_"+journey.abbreviation+"salle"
        +this.form.value.salle+"de"+this.form.value.from+"a"
        +this.form.value.to+"session"+this.form.value.session+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
      this.isvisible = false
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

  async ngOnInit(){
    const data = [];
    for (let i = 0; i < 100; i++) {
      data.push({
        name: 'John Brown',
        age: i + 1,
        street: 'Lake Park',
        building: 'C',
        number: 2035,
        companyAddress: 'Lake Street 42',
        companyName: 'SoftLake Co',
        gender: 'M'
      });
    }
    this.listOfData = data;
    // get College year
    this.allYears = await this.service.getCollegeYear().toPromise()
    // get mention by permission
    if(this.authService.getPermission()){
      this.allMention = await this.service.getMentionUser()
      this.allJourney = await this.service.getAllJourney(localStorage.getItem('mention')).toPromise()
      this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem('journey'))?.semester
      this.getStorage()
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()

      if(testNote){
        this.getNoteMatier()
        this.form.get('filter')?.setValue('Credit')
        console.log(this.form.value.filter)
        this.showTable = true
      }else{
        this.showTable = false
    }

    }else{
      this.form.get('salle')?.clearValidators()
      this.form.get('from')?.clearValidators()
      this.form.get('to')?.clearValidators()

      this.allMention = await this.service.getMentionAdmin().toPromise()
      this.form.get('collegeYear')?.setValue(this.allYears[0].title)
      this.form.get('mention')?.setValue(this.allMention[0].uuid)
      this.form.get('session')?.setValue('Normal')

      this.allJourney = await this.service.getAllJourney(this.form.value.mention).toPromise()
      this.form.get('semester')?.setValue(this.allJourney[1].semester[0])
      this.form.get('journey')?.setValue(this.allJourney[1].uuid)
      this.listOfSemester = this.allJourney[1].semester

      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      if(testNote){
        this.getNoteMatier()
        this.showTable = true
      }else{
        this.showTable = false
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
    }

  }      

  showConfirmStudent(numCarte: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+numCarte+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/notes/student?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&num_carte='
        +numCarte+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.listOfDisplayData = [...data]},
          error => console.error("error as ", error)
        );
      }
    })
  }


  
  deleteTable(): void{
    const journey = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer la table note "+this.form.get('semester')?.value+" "+journey?.abbreviation+" "+this.form.get('session')?.value+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/notes/?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          error => console.error("error as ", error)
        );
      }
    })
  }

  insertStudent(): void{
    if (this.form.valid) {
        this.http.post<any>(`${BASE_URL}/notes/insert_students/?college_year=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_mention='
        +this.form.get('mention')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.listOfDisplayData = [... data]
          },
          error => console.error("error as ", error)
        );
      }
  }

  submitForm(): void {
    this.showStep = true
    if (this.form.valid) {
      this.isConfirmLoading = true
        this.http.post<any>(`${BASE_URL}/notes/?college_year=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.allColumns = data
            this.listOfDisplayData = [...this.allStudents]
          },
          error => console.error("error as ", error)
        )
      
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
      this.allJourney = await this.service.getAllJourney(this.form.value.mention).toPromise()
    }
  }
  async changeJourney(){
    if(this.form.value.journey ){
      localStorage.setItem('journey', this.form.value.journey)
      this.listOfSemester = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem('journey'))?.semester
      console.log(this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem('journey'))?.semester, this.form.value.journey, this.allJourney)
    }
  }
  async getAllColumnsSession(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('semester')?.value){
      this.setLocalStore()
      console.log(this.matier)
      let testNote: boolean = await this.noteService.testNote( 
        this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
        if(testNote){
          this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
          this.getNoteMatier()
          this.showTable = true
        }else{
          this.matier = []
          this.showTable = false
          this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
      }
    }
  }

  async setLocalStore(){
    localStorage.setItem('collegeYear', this.form.value.collegeYear)
    localStorage.setItem('journey', this.form.value.journey)
    localStorage.setItem('mention', this.form.value.mention)
    localStorage.setItem('semester', this.form.value.semester)
    localStorage.setItem('session', this.form.value.session)
    localStorage.setItem('filter', this.form.value.filter)
  }
  async getNoteMatier(){
    this.isSpinning = true 
    this.matierEc = await this.service.getEc(this.form.value.semester, this.form.value.journey).toPromise()
    this.matierUe = await this.service.getUe(this.form.value.semester, this.form.value.journey).toPromise()
    let data = await this.noteService.getAllColumns(this.form.value.semester, this.form.value.journey,
       this.form.value.session, this.form.value.collegeYear).toPromise()
    this.allColumns = data
    this.allColumnUe = []
    this.allColumnEc = []
    console.log(data)
    for (let i=0; i<data.length; i++){
        const name = this.matierUe.find((item:Ue) => item.value ===  data[i]['name'])
        this.allColumnUe.push({name: name?.title, value: data[i]['name'], nbr_ec: data[i]['nbr_ec'] })
        let ec = data[i]['ec']
        for (let j=0; j<ec.length; j++){
          console.log(ec[j])
          const name = this.matierEc.find((item:Ec) => item.value ===  ec[j]['name'])
          this.allColumnEc.push({name: name?.title, value: ec[j]['name'] })
        }
    }
       
    this.allStudents = await this.noteService.getAllNote(
      this.form.value.semester, 
      this.form.value.journey, 
      this.form.value.session, 
      this.form.value.collegeYear).toPromise(),
    this.isSpinning = false
    this.listOfDisplayData = [...this.allStudents]
    this.updateEditCache()
     
  }
  async refresh(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value){
      this.setLocalStore()
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      if(testNote){
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
      }else{
        this.matier = []
        this.showTable = false
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
    }
    }
  }

  async getAllColumnsSemester(){
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value){
      this.setLocalStore()
      let testNote: boolean = await this.noteService.testNote(this.form.value.semester, this.form.value.journey, this.form.value.session).toPromise()
      if(testNote){
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
        this.getNoteMatier()
        this.showTable = true
      }else{
        this.matier = []
        this.showTable = false
        this.matier = await this.service.getMatier(this.form.value.collegeYear, this.form.value.semester, this.form.value.journey).toPromise()
    }
    }
  }


  getAllJourney(): void{
    this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
      data => {
          console.error("error as ", data)
          this.allJourney = data
          this.form.get('journey')?.setValue('')
      },
      error => {
        this.allJourney = []
        console.error("error as ", error)
      }
    )
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

