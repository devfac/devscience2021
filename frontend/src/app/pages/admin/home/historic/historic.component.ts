import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { typeTitleUser, typeTitleAdmin } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams, otherQueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { TableHeader } from '@app/models/table';
import { Ue } from '@app/models/ue';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from '../college-year/college-year.service';
import { DroitService } from '../droit/droit.service';
import { MentionService } from '../mention/mention.service';
import { HistoricService } from './historic.service';
import { User } from '@app/models';

const CODE = "historic"

@Component({
  selector: 'app-historic',
  templateUrl: './historic.component.html',
  styleUrls: ['./historic.component.less']
})
export class HistoricComponent implements OnInit {

  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];
  childrenDataHeader: TableHeader[] = [];
  allYears: CollegeYear[] = []
  allTitle: Mention[] = []
  allUe: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  form_years!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  typeTitle = [{label:'', value:''}];
  actualYear: string | null = ""
  titles: any[] = []
  actions = {
    add: false,
    edit: false,
    delete: false,
    detail: false,
  };
  
  keyYear = CODE+"collegeYear"
  keyTitle = CODE+"title"
  isInit: boolean = false
  user!: User
  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: HistoricService
    ) { 
      this.form = this.fb.group({
        collegeYear: [null],
        title: [null],
      });}

  async ngAfterContentInit() {
    this.headers = [
    {
      title: 'Email',
      selector: 'email',
      isSortable: true,
    },{
      title: 'Titre',
      selector: 'title',
      isSortable: true,
    },
    {
      title: 'Création date',
      selector: 'created_at',
      isSortable: true,
    }
  ];
  this.childrenDataHeader = [
    {
      title: 'Création date',
      selector: 'created_at',
      isSortable: true,
    }
  ];

  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)

    let allYears: ResponseModel = await this.serviceYears.getDataPromise().toPromise()
    this.allYears = allYears.data
    this.user = await this.service.getMe().toPromise()
    if(this.user.is_superuser){
      this.typeTitle = typeTitleAdmin
    }else{
      this.typeTitle = typeTitleUser
    }
    this.testStorage(this.keyYear, this.allYears[0].title)
    this.testStorage(this.keyTitle, this.typeTitle[0].value)
  }

  fetchData(params?: QueryParams){
    let otherParams: otherQueryParams = {
      college_year: localStorage.getItem(this.keyYear),
      title: localStorage.getItem(this.keyTitle),
    }
    return this.service.getDataObservable(parseQueryParams(params, otherParams))
  }

  changeYear(){
    if(this.form.value.collegeYear){
    localStorage.setItem(this.keyYear, this.form.value.collegeYear)
    this.datatable.fetchData()
  }
}
changeTitle(){
  if(this.form.value.title){
  localStorage.setItem(this.keyTitle, this.form.value.title)
  this.datatable.fetchData()
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

  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: async () => {
        await this.service.deletData(uuid)
        this.datatable.fetchData()
      }
    })
  }

  onDelete(row: any) {
    console.log(row);
    this.showConfirm(row.mention.abbreviation+" "+row.level+" "+row.year, row.uuid);
  }

  handleCancel(): void{
    this.isvisible = false
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }
}
