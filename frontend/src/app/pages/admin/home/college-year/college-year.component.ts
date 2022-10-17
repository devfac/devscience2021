import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-college-year',
  templateUrl: './college-year.component.html',
  styleUrls: ['./college-year.component.less']
})
export class CollegeYearComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })


  
  allYear: CollegeYear[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  isDisabled: boolean = false

  options = {
    headers: this.headers
  }

  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder) { }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    this.http.get<any>(`${BASE_URL}/college_year/`, options).subscribe(
      data => this.allYear = data,
      error => console.error("error as ", error)
    );

    this.form = this.fb.group({
      title: [null, [Validators.required]],
      mean: [null, [Validators.required]],
    });
  }

  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/mentions/?uuid=`+uuid, this.options).subscribe(
          data => this.allYear = data,
          error => console.error("error as ", error)
        );
      }
    })
  }

  
  submitForm(): void {
    if (this.form.valid) {
      const title = this.form.value.title
      const mean = this.form.value.mean
      this.isConfirmLoading = true
      const body = {
        mean: mean
      }
      if (this.isEdit){
        this.http.put<any>(`${BASE_URL}/college_year/?uuid=`+this.uuid, body, this.options).subscribe(
          data => this.allYear = data,
          error => console.error("error as ", error)
        )
      }else{
        this.http.post<any>(`${BASE_URL}/college_year/`,body, this.options).subscribe(
          data => this.allYear = data,
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
    this.form.get('mean')?.setValue('');
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/college_year/`+uuid, this.options).subscribe(
      data => {
        console.error(data)
        this.form.get('title')?.setValue(data.title),
        this.form.get('mean')?.setValue(data.mean)
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

