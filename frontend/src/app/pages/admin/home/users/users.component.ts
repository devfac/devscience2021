import { Component, OnInit } from '@angular/core';
import { User } from '@app/models';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from "ng-zorro-antd/modal";
import { Role } from '@app/models/role';
import { Mention } from '@app/models/mention';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators } from '@angular/forms';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.less']
})

export class UsersComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  allUsers: User[] = []
  allRole: Role[] = []
  allMention: Mention[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";

  options = {
    headers: this.headers
  }
  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder) { }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    
    this.http.get<any>(`${BASE_URL}/users/get_all`, this.options).subscribe(
      data => this.allUsers = data,
      error => console.error("error as ", error)
    );
    this.http.get<any>(`${BASE_URL}/roles/`, options).subscribe(
      data => this.allRole = data,
      error => console.error("error as ", error)
    );

    this.http.get<any>(`${BASE_URL}/mentions/`, this.options).subscribe(
      data =>{
        this.allMention = data
        },
        error => console.error("error as ", error)
    );
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
  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/users/?uuid=`+uuid, this.options).subscribe(
          data => this.allUsers = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  confirmPassword: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
    const password = this?.form?.get('password')?.value;
    const confirm_password = control.value;
    return password === confirm_password ? null : { mismatch: true };
  }


  submitForm(): void {
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
        this.http.put<any>(`${BASE_URL}/users/?uuid=`+this.uuid, data, this.options).subscribe(
          data => this.allUsers = data,
          error => console.error("error as ", error)
        )
      }else{
        console.error(data1)
        this.http.post<any>(`${BASE_URL}/users/`,data1, this.options).subscribe(
          data => this.allUsers = data,
          error => console.error("error as ", error)
        )
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

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.form.get('password')?.clearValidators()
    this.form.get('confirmPassword')?.clearValidators()
    this.uuid = uuid
    this.http.get<User>(`${BASE_URL}/users/by_uuid/`+uuid, this.options).subscribe(
      data => {
        console.error(data)
        this.form.get('email')?.setValue(data.email);
        this.form.get('isAdmin')?.setValue(data.is_admin);
        this.form.get('isActive')?.setValue(data.is_active);
        this.form.get('firstName')?.setValue(data.first_name);
        this.form.get('lastName')?.setValue(data.last_name);
        this.form.get('isActive')?.setValue(data.is_active);
        this.form.get('isAdmin')?.setValue(data.is_admin);
        this.form.get('uuidMention')?.setValue(data.uuid_mention);
        this.form.get('uuidRole')?.setValue(data.uuid_role);
      },
      error => console.error("error as ", error)
    );
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
