import { HttpHeaders, HttpClient } from '@angular/common/http';
import { AfterContentInit, Component, OnInit, TemplateRef, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey} from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams, otherQueryParams } from '@app/models/query';
import { AncienStudent, StudentColumn, ColumnItem  } from '@app/models/student';
import { TableHeader } from '@app/models/table';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { DownloadService } from '../../download.service';
import { CollegeYearService } from '../../home/college-year/college-year.service';
import { JourneyService } from '../../home/journey/journey.service';
import { MentionService } from '../../home/mention/mention.service';
import { SelectionService } from './selection.service';

const BASE_URL = environment.authApiURL;
const CODE = "selection"

@Component({
  selector: 'app-selection',
  templateUrl: './selection.component.html',
  styleUrls: ['./selection.component.less']
})
export class SelectionComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  @ViewChild('isSelected', { static: true }) isSelected!: TemplateRef<any>;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  allStudents: AncienStudent[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  formList!: FormGroup
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  data = ""
  uuid= "";
  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numSelect"
  isLoading: boolean = false

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public router: Router, 
    private downloads: DownloadService,
    private authUser: AuthService,
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: SelectionService,
    ) { 


    this.form = this.fb.group({
      email: [null, [Validators.required]],
      firstName: [null, [Validators.required]],
      lastName: [null, [Validators.required]],
      isAdmin: [false],
      mention: [null],
      collegeYear: [null],
      uuidRole: [null, [Validators.required]],
      uuidMention: [[], [Validators.required]],
    });
  }

  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Num Select',
      selector: 'num_select',
      isSortable: true,
    },{
      title: 'Nom',
      selector: 'last_name',
      width:"280px",
      isSortable: true,
    },{
      title: 'Prenom',
      selector: 'first_name',
      isSortable: true,
    },{
      title: 'Séléctioné',
      selector: 'is_selected',
      template: this.isSelected,
      isSortable: false,
    },
  ]
  }
  
  async ngOnInit() {
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
    
    this.allYears = await this.serviceYears.getDataPromise().toPromise()
    
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
    console.log(key.substring(CODE.length), value)
    return true
  }

  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      uuid_mention: localStorage.getItem(this.keyMention),
    }
    return this.service.getDataObservable(parseQueryParams(params,otherParams))
  }
  showConfirm(name: string, numSelect: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: async () => {
        await this.service.deletData(numSelect)
        this.datatable.fetchData()
      }
    })
  }
  
  onDelete(row: any) {
    this.showConfirm(row.title, row.uuid);
  }

  onEdit(row: any) {
    this.showModalEdit(row.num_select);
  }

  onAdd() {
    this.addStudent();
  }
  
  showModalEdit(numSelect: string): void{
    this.isEdit = true
    localStorage.setItem(this.keyNum, numSelect)
    localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
    localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
    this.router.navigate(['/user/selection_add'])
  }
  download(){

  }
  /*
  download(): void {
    const url: string = `${BASE_URL}/liste/list_selection/?college_year=`+this.form.get('collegeYear')?.value+`&uuid_mention=`+this.form.get('mention')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        a.download = 'etudiants_séléctioné.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }
*/
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
    localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
    localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
    localStorage.setItem(this.keyNum, '')
    this.router.navigate(['/user/selection_add'])
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }



}
