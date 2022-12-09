import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { typeLevel } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { otherQueryParams, QueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { AncienStudent } from '@app/models/student';
import { TableHeader } from '@app/models/table';
import { AuthService } from '@app/services/auth/auth.service';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from '../../home/college-year/college-year.service';
import { JourneyService } from '../../home/journey/journey.service';
import { MentionService } from '../../home/mention/mention.service';
import { InscriptionService } from './inscription.service';

const CODE = "inscription"

@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.less']
})
export class InscriptionComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];


  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  allStudents: AncienStudent[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  data = ""
  uuid= "";
  listOfData: any[] = []
  keyMention = CODE+"mention"
  keyYear = CODE+"collegeYear"
  keyNum = CODE+"numSelect"
  keyLevel = CODE+"level"
  isLoading: boolean = false
  typelevel = typeLevel

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  
  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public router: Router, 
    private authUser: AuthService, 
    private serviceJourney: JourneyService,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: InscriptionService,
    ) { 


    this.form = this.fb.group({
      collegeYear: [null],
      journey: [null, [Validators.required]],
      mention: [null, [Validators.required]],
      level: [null],
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
      width:"250px",
      isSortable: true,
    },{
      title: 'Prenom',
      selector: 'first_name',
      isSortable: true,
    },{
      title: 'Niveau',
      selector: 'level',
      isSortable: true,
    },{
      title: 'Parcours',
      selector: 'journey.abbreviation',
      isSortable: false,
    },
  ];
  }

 async ngOnInit() {
    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let mention = await this.serviceMention.getData(user?.uuid_mention[i]).toPromise()
      this.allMention.push(mention)
          
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
      level: localStorage.getItem(this.keyLevel),
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
    this.router.navigate(['/user/inscription_add'])
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

  changeLevel(): void{
    if(this.form.get(this.keyYear.substring(CODE.length))?.value && 
    this.form.get(this.keyMention.substring(CODE.length))?.value && this.isLoading){
      localStorage.setItem(this.keyYear, this.form.get(this.keyYear.substring(CODE.length))?.value)
      localStorage.setItem(this.keyMention, this.form.get(this.keyMention.substring(CODE.length))?.value)
      localStorage.setItem(this.keyLevel, this.form.get(this.keyLevel.substring(CODE.length))?.value)
      this.datatable.fetchData()
    }
  }

  addStudent():void{
    localStorage.setItem(this.keyNum, '')
    this.router.navigate(['/user/inscription_add'])
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }
}
