import { AfterContentInit, Component, OnInit, ViewChild } from '@angular/core';
import { User } from '@app/models';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from "ng-zorro-antd/modal";
import { Role } from '@app/models/role';
import { Mention } from '@app/models/mention';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';
import { UsersService } from './users.service';
import { TableHeader } from '@app/models/table';
import { DatatableCrudComponent } from '@app/shared/components/datatable-crud/datatable-crud.component';
import { MentionService } from '../mention/mention.service';
import { RoleService } from '../role/role.service';
import { QueryParams } from '@app/models/query';
import { parseQueryParams } from '@app/shared/utils';
import { ResponseModel } from '@app/models/response';



@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.less']
})

export class UsersComponent implements OnInit, AfterContentInit {
  @ViewChild(DatatableCrudComponent) datatable!: DatatableCrudComponent;
  headers: TableHeader[] = [];

  allRole: Role[] = []
  allMention: Mention[] = []
  confirmModal?: NzModalRef
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
    private service: UsersService,
    private serviceMention: MentionService,
    private roleService: RoleService
    ) {
      this.form = this.fb.group({
        email: [null, [Validators.required]],
        firstName: [null, [Validators.required]],
        lastName: [null, [Validators.required]],
        isAdmin: [false],
        isActive: [false],
        password: [null],
        uuidRole: [null, [Validators.required]],
        uuidMention: [[], [Validators.required]],
      });
     }

  ngAfterContentInit(): void {
    this.headers = [
        {
          title: 'Email',
          selector: 'email',
          isSortable: true,
        },
        {
          title: 'Nom',
          selector: 'last_name',
          isSortable: true,
        },
        {
          title: 'Prenom',
          selector: 'first_name',
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
    let allMention: ResponseModel = await this.serviceMention.getDataPromise().toPromise()
    this.allMention = allMention.data
    this.allRole = await this.roleService.getDataPromise().toPromise()
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

  confirmPassword: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const password = this?.form?.get('password')?.value;
    const confirm_password = control.value;
    return password === confirm_password ? null : { mismatch: true };
  }

  onDelete(row: any) {
    this.showConfirm(row.email, row.uuid);
  }

  onEdit(row: any) {
    this.showModalEdit(row.uuid);
  }

  onAdd() {
    this.showModal();
  }
  

  async submitForm(){
    if (this.form.valid) {
      const email = this.form.value.email
      const password = this.form.value.password
      const firstName = this.form.value.firstName
      const lastName = this.form.value.lastName
      const uuidMention = this.form.value.uuidMention
      const uuidRole = this.form.value.uuidRole
      const isActive = this.form.value.isActive
      const isAdmin = this.form.value.isAdmin

      let data1 = {
          "email": email,
          "is_active": isActive,
          "is_admin": isAdmin,
          "is_superuser": false,
          "first_name": firstName,
          "last_name": lastName,
          "uuid_mention": uuidMention,
          "uuid_role": uuidRole,
          "password": password
      }

      let data2 = {
        "email": email,
        "is_active": isActive,
        "is_admin": isAdmin,
        "is_superuser": false,
        "first_name": firstName,
        "last_name": lastName,
        "uuid_mention": uuidMention,
        "uuid_role": uuidRole,
      }

      this.isConfirmLoading = true
      if (this.isEdit){
        var data = null
        if (password){
          data = data1
        }else{
          data = data2
        }
        await this.service.updateData(this.uuid, data).toPromise()
        this.datatable.fetchData()
        
      }else{
        await this.service.addData(data1).toPromise()
        this.datatable.fetchData()
        
      }
      
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

  showModal(): void{
    this.isEdit = false;
    this.isvisible = true;
    this.form.get('password')?.setValidators(Validators.required)
    this.form.get('confirmPassword')?.setValidators(this.confirmPassword)
    this.form.get('email')?.setValue(null);
    this.form.get('firstName')?.setValue('');
    this.form.get('lastName')?.setValue('');
    this.form.get('isActive')?.setValue(false);
    this.form.get('isAdmin')?.setValue(false);
    this.form.get('password')?.setValue('');
    this.form.get('confirmPassword')?.setValue('');
    this.form.get('uuidMention')?.setValue([]);
    this.form.get('uuidRole')?.setValue('');
  }

 async showModalEdit(uuid: string){
    this.isEdit = true
    this.form.get('password')?.clearValidators()
    this.form.get('confirmPassword')?.clearValidators()
    this.uuid = uuid
    let data: any = await this.service.getData(uuid).toPromise()
    this.form.get('email')?.setValue(data.email);
    this.form.get('isAdmin')?.setValue(data.is_admin);
    this.form.get('isActive')?.setValue(data.is_active);
    this.form.get('firstName')?.setValue(data.first_name);
    this.form.get('lastName')?.setValue(data.last_name);
    this.form.get('isActive')?.setValue(data.is_active);
    this.form.get('isAdmin')?.setValue(data.is_admin);
    this.form.get('uuidMention')?.setValue(data.uuid_mention);
    this.form.get('uuidRole')?.setValue(data.uuid_role);
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
