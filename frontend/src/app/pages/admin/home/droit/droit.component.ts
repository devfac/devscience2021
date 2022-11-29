import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { typeLevel } from '@app/data/data';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams } from '@app/models/query';
import { TableHeader } from '@app/models/table';
import { Ue } from '@app/models/ue';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from '../college-year/college-year.service';
import { JourneyService } from '../journey/journey.service';
import { MentionService } from '../mention/mention.service';
import { UeService } from '../ue/ue.service';
import { DroitService } from './droit.service';

@Component({
  selector: 'app-droit',
  templateUrl: './droit.component.html',
  styleUrls: ['./droit.component.less']
})
export class DroitComponent implements OnInit {

  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  user = localStorage.getItem('user')
  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
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
  typeLevel = typeLevel;
  actualYear: string | null = ""
  titles: any[] = []
  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };
  
  isInit: boolean = false
  constructor(
    private modal: NzModalService, 
    private fb: FormBuilder,
    private serviceMention: MentionService,
    private serviceYears: CollegeYearService,
    private service: DroitService
    ) { 
      this.form = this.fb.group({
        droit: [null, [Validators.required]],
        level: [null, [Validators.required]],
        mention: [null, [Validators.required]],
        collegeYear: [null, [Validators.required]],
      });}

  async ngAfterContentInit() {
    this.headers = [
    {
      title: 'Niveau',
      selector: 'level',
      isSortable: true,
    },{
      title: 'Droit',
      selector: 'droit',
      isSortable: true,
    },{
      title: 'Anne',
      selector: 'year',
      isSortable: true,
    },{
      title: 'Mention',
      selector: 'mention.title',
      isSortable: true,
    },
  ];

  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)

    this.allMention = await this.serviceMention.getDataPromise().toPromise()
    this.testStorage('mention', this.allMention[0].uuid)
    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }

    this.allYears = await this.serviceYears.getDataPromise().toPromise()
    this.testStorage('collegeYear', this.allYears[0].title)
    this.actualYear = localStorage.getItem('collegeYear')
  }
  fetchData(params?: QueryParams){
    return this.service.getDataObservable(parseQueryParams(params))
  }
  testStorage(key: string, value: string){
    if(localStorage.getItem(key)){
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }else{
      localStorage.setItem(key, value)
      this.form.get(key)?.setValue(localStorage.getItem(key))
    }
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
    this.showConfirm(row.title, row.uuid);
  }

  onEdit(row: any) {
    this.showModalEdit(row.uuid);
  }

  onAdd() {
    this.showModal();
  }

  async submitForm(){
    if (this.form.valid) {
      const data = {
        droit: this.form.value.droit, 
        level: this.form.value.level, 
        year: this.form.value.collegeYear, 
        uuid_mention: this.form.value.mention
      }

      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        await this.service.updateData(this.uuid, data).toPromise()
        this.datatable.fetchData()
      }else{
        await this.service.addData(data).toPromise()
        this.datatable.fetchData()
      }
      
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

  showModal(): void{
    this.isEdit = false;
    this.isvisible = true;
    this.form.get('droit')?.setValue('');
    this.form.get('level')?.setValue('');
    this.form.get('mention')?.setValue('');
    this.form.get('collegeYear')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('droit')?.setValue(data.droit),
    this.form.get('level')?.setValue(data.level),
    this.form.get('mention')?.setValue(data.uuid_mention),
    this.form.get('collegeYear')?.setValue(data.year)
    this.isvisible = true
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
