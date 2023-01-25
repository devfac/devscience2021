import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Mention } from '@app/models/mention';
import { QueryParams } from '@app/models/query';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { HomeService } from '../home.service';
import { MentionService } from './mention.service';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-mention',
  templateUrl: './mention.component.html',
  styleUrls: ['./mention.component.less']
})
export class MentionComponent implements OnInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  
  allMention: Mention[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
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
    private service: MentionService,
    ) {
      this.form = this.fb.group({
        title: [null, [Validators.required]],
        abbreviation: [null, [Validators.required]],
        plugged: [null, [Validators.required]],
        last_num_carte: [null, [Validators.required]],
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
            title: 'Abbreviation',
            selector: 'abbreviation',
            isSortable: true,
          },
          {
            title: 'Branche',
            selector: 'plugged',
            isSortable: true,
          },{
            title: 'LastCe',
            selector: 'last_num_carte',
            isSortable: true,
          },
        ];
    }
  
  async ngOnInit(){
    this.fetchData = this.fetchData.bind(this)
  }

  fetchData(params?: QueryParams){
    return this.service.getDataObservable(parseQueryParams(params))
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
      const title = this.form.value.title
      const abbreviation = this.form.value.abbreviation
      const plugged = this.form.value.plugged
      const last_num_carte = this.form.value.last_num_carte
      this.isConfirmLoading = true
      const body = {
        title: title,
        abbreviation: abbreviation,
        plugged: plugged,
        last_num_carte: last_num_carte,
      }
      if (this.isEdit){
        await this.service.updateData(this.uuid, body).toPromise()
        this.datatable.fetchData()
        
      }else{
        await this.service.addData(body).toPromise()
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
    this.form.get('plugged')?.setValue('');
    this.form.get('last_num_carte')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title);
    this.form.get('abbreviation')?.setValue(data.abbreviation);
    this.form.get('plugged')?.setValue(data.plugged);
    this.form.get('last_num_carte')?.setValue(data.last_num_carte);
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
