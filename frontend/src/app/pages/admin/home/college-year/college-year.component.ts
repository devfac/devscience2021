import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { QueryParams } from '@app/models/query';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { parseQueryParams } from '@app/shared/utils';
import { environment } from '@environments/environment';
import { truncate } from 'lodash';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { CollegeYearService } from './college-year.service';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-college-year',
  templateUrl: './college-year.component.html',
  styleUrls: ['./college-year.component.less']
})
export class CollegeYearComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  isDisabled: boolean = false
  actions = {
    add: true,
    edit: true,
    delete: true,
    detail: false,
  };

  constructor(
    public service: CollegeYearService, 
    private modal: NzModalService, 
    private fb: FormBuilder) { 

    this.form = this.fb.group({
      title: [null, [Validators.required]],
      mean: [null, [Validators.required]],
    });
    }
    ngOnInit(): void {
      this.fetchData = this.fetchData.bind(this)
    }
  
    fetchData(params?: QueryParams){
      return this.service.getDataObservable(parseQueryParams(params))
    }

    ngAfterContentInit(): void {
      this.headers = [
        {
          title: 'Titre',
          selector: 'title',
          isSortable: true,
        },
        {
          title: 'Code',
          selector: 'code',
          isSortable: true,
        },
        {
          title: 'Moyenne',
          selector: 'mean',
          isSortable: true,
        },
      ];
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
      const mean = this.form.value.mean
      this.isConfirmLoading = true
      
      if (this.isEdit){
        const body = {
        mean: mean
        }
        await this.service.updateData(this.uuid, body).toPromise()
        this.datatable.fetchData()
      }else{
        const body = {
          title: this.form.value.title, 
          mean: mean
        }
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
    this.form.get('mean')?.setValue('');
  }

  async showModalEdit(uuid: string){
    this.isEdit = true
    this.uuid = uuid
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('title')?.setValue(data.title),
    this.form.get('mean')?.setValue(data.mean)
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

