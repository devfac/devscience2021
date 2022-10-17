import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Role } from '@app/models/role';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';


const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-role',
  templateUrl: './role.component.html',
  styleUrls: ['./role.component.less']
})
export class RoleComponent implements OnInit {

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  allRole: Role[] = []
  confirmModal?: NzModalRef;
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
    this.http.get<any>(`${BASE_URL}/roles/`, options).subscribe(
      data => this.allRole = data,
      error => console.error("error as ", error)
    );

    this.form = this.fb.group({
      title: [null, [Validators.required]],
    });
  }

  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/roles/?uuid=`+uuid, this.options).subscribe(
          data => this.allRole = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  submitForm(): void {
    if (this.form.valid) {
      const title = this.form.value.title
      this.isConfirmLoading = true
      const body = {
        title: title
      }
      if (this.isEdit){
        this.http.put<any>(`${BASE_URL}/roles/?uuid=`+this.uuid, body, this.options).subscribe(
          data => this.allRole = data,
          error => console.error("error as ", error)
        )
      }else{
        this.http.post<any>(`${BASE_URL}/roles/`,body, this.options).subscribe(
          data => this.allRole = data,
          error => console.error("error as ", error)
        )
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

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/roles/`+uuid, this.options).subscribe(
      data => this.form.get('title')?.setValue(data.title),
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
