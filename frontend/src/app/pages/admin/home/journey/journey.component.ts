import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { QueryParams } from '@app/models/query';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { MentionService } from '../mention/mention.service';
import { JourneyService } from './journey.service';
import { parseQueryParams } from '@app/shared/utils';
import { ResponseModel } from '@app/models/response';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-journey',
  templateUrl: './journey.component.html',
  styleUrls: ['./journey.component.less']
})
export class JourneyComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  allJourney: Journey[] = []
  allMention: Mention[] = []
  listOfOptions = ['S1' ,'S2' ,'S3' ,'S4' ,'S5' ,'S6' ,'S7' ,'S8' ,'S9' ,'S10']
  semesterTitles: any[] = []
  listOfTagsOptions =[]
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  uuid= '';

  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };

  constructor(
    private modal: NzModalService,
    private fb: FormBuilder,
    private service: JourneyService,
    private serviceMention: MentionService
    ) {  this.form = this.fb.group({
      title: [null, [Validators.required]],
      abbreviation: [null, [Validators.required]],
      uuidMention: [null, [Validators.required]],
      semesterList: [['S1'], [Validators.required]],
    });
}
  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Title',
      selector: 'title',
      isSortable: true,
    },
    {
      title: 'Abbréviation',
      selector: 'abbreviation',
      width:'150px',
      isSortable: true,
    },
    {
      title: 'Semestre',
      selector: 'semester',
      width:'120px',
      isSortable: true,
    },
    {
      title: 'Mention',
      selector: 'mention.abbreviation',
      isSortable: true,
    },
  ];
  }

  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)
   let allMention: ResponseModel = await this.serviceMention.getDataPromise().toPromise()
   this.allMention = allMention.data
  }

  fetchData(params?: QueryParams){
    return this.service.getDataObservable(parseQueryParams(params))
  }

  showConfirm(name: string, uuid: string){
    this.confirmModal = this.modal.confirm({
      nzTitle: 'Voulez-vous supprimer '+name+'?',
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
        title: this.form.value.title,
        semester: this.form.value.semesterList,
        uuid_mention: this.form.value.uuidMention,
        abbreviation: this.form.value.abbreviation
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
    this.form.get('title')?.setValue('');
    this.form.get('abbreviation')?.setValue('');
    this.form.get('uuidMention')?.setValue('');
    this.form.get('semesterList')?.setValue([]);
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title),
    this.form.get('abbreviation')?.setValue(data.abbreviation),
    this.form.get('uuidMention')?.setValue(data.mention.uuid),
    this.form.get('semesterList')?.setValue(data.semester)
    console.error(data.semester)
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
