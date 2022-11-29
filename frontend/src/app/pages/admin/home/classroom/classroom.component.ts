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
import { DroitService } from '../droit/droit.service';
import { MentionService } from '../mention/mention.service';
import { ClassroomService } from './classroom.service';

@Component({
  selector: 'app-classroom',
  templateUrl: './classroom.component.html',
  styleUrls: ['./classroom.component.less']
})
export class ClassroomComponent implements OnInit {

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
    private service: ClassroomService
    ) { 
      this.form = this.fb.group({
        name: [null, [Validators.required]],
        capacity: [null, [Validators.required]],
      });}

  async ngAfterContentInit() {
    this.headers = [
    {
      title: 'Salle',
      selector: 'name',
      isSortable: true,
    },{
      title: 'Capacité',
      selector: 'capacity',
      isSortable: true,
    }
  ];

  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)
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
    this.showConfirm(row.name, row.uuid);
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
        name: this.form.value.name, 
        capacity: this.form.value.capacity
      }

      this.isConfirmLoading = true
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
    this.form.get('name')?.setValue('');
    this.form.get('capacity')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('name')?.setValue(data.name),
    this.form.get('capacity')?.setValue(data.capacity)
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
