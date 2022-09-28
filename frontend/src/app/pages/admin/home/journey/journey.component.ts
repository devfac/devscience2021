import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-journey',
  templateUrl: './journey.component.html',
  styleUrls: ['./journey.component.less']
})
export class JourneyComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })


  
  all_journey: Journey[] = []
  all_mention: Mention[] = []
  listOfOptions = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  listOfTagsOptions =[] 
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  data = ""

  options = {
    headers: this.headers
  }

  constructor(private http: HttpClient,  private modal: NzModalService, private fb: FormBuilder) { }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    this.http.get<any>(`${BASE_URL}/journey/`, options).subscribe(
      data => this.all_journey = data,
      error => console.error("error as ", error)
    );

    this.http.get<any>(`${BASE_URL}/mentions/`, this.options).subscribe(
      data =>{
        this.all_mention = data
        },
        error => console.error("error as ", error)
    );

    this.form = this.fb.group({
      title: [null, [Validators.required]],
      abbreviation: [null, [Validators.required]],
      uuid_mention: [null, [Validators.required]],
      semester: [[], [Validators.required]],
    });

  }
  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/mentions/?uuid=`+uuid, this.options).subscribe(
          data => this.all_journey = data,
          error => console.error("error as ", error)
        );
      }
    })
  }
  submitForm(): void {
    if (this.form.valid) {
      const data = this.form.getRawValue()
      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        this.http.put<any>(`${BASE_URL}/journey/?uuid=`+this.uuid, data, this.options).subscribe(
          data => this.all_journey = data,
          error => console.error("error as ", error)
        )
      }else{
        this.http.post<any>(`${BASE_URL}/journey/`,data, this.options).subscribe(
          data => this.all_journey = data,
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
    this.form.get('abbreviation')?.setValue('');
    this.form.get('uuid_mention')?.setValue('');
    this.form.get('semester')?.setValue([""]);
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/journey/by_uuid/`+uuid, this.options).subscribe(
      data => {
        this.form.get('title')?.setValue(data.title),
        this.form.get('abbreviation')?.setValue(data.abbreviation),
        this.form.get('uuid_mention')?.setValue(data.mention.uuid),
        this.form.get('semester')?.setValue(data.semester)
        console.error(data.mention.title)
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
