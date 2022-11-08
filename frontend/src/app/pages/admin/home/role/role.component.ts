import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QueryParams } from '@app/models/query';
import { Role } from '@app/models/role';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { RoleService } from './role.service';


@Component({
  selector: 'app-role',
  templateUrl: './role.component.html',
  styleUrls: ['./role.component.less']
})
export class RoleComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  allRole: Role[] = []
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
    private modal: NzModalService, 
    private fb: FormBuilder,
    private service: RoleService
    ) {
      this.form = this.fb.group({
        title: [null, [Validators.required]],
      }); }

  ngAfterContentInit(): void {
    this.headers = [
    {
      title: 'Title',
      selector: 'title',
      isSortable: true,
    },
  ];
}

  ngOnInit(): void {
    this.fetchData = this.fetchData.bind(this)
  }

  fetchData(params?: QueryParams){
    return this.service.getDataObservable(parseQueryParams(params))
  }

  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.service.deletData(uuid)
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
      this.isConfirmLoading = true
      const body = {
        title: title
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
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
      let data: any = await this.service.getData(uuid).toPromise()
      this.form.get('title')?.setValue(data.title),
     
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
