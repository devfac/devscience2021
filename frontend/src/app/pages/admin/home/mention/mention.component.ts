import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Mention } from '@app/models/mention';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-mention',
  templateUrl: './mention.component.html',
  styleUrls: ['./mention.component.less']
})
export class MentionComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  all_mention: Mention[] = []
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
  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder,) { }

  ngOnInit(): void {
    this.http.get<any>(`${BASE_URL}/mentions/`, this.options).subscribe(
      data => this.all_mention = data,
      error => console.error("error as ", error)
    );

    this.form = this.fb.group({
      title: [null, [Validators.required]],
      abbreviation: [null, [Validators.required]],
      plugged: [null, [Validators.required]],
      last_num_carte: [null, [Validators.required]],
    });
  }
  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/mentions/?uuid=`+uuid, this.options).subscribe(
          data => this.all_mention = data,
          error => console.error("error as ", error)
        );
      }
    })
  }
  submitForm(): void {
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
        this.http.put<any>(`${BASE_URL}/mentions/?uuid=`+this.uuid, body, this.options).subscribe(
          data => this.all_mention = data,
          error => console.error("error as ", error)
        )
      }else{
        this.http.post<any>(`${BASE_URL}/mentions/`,body, this.options).subscribe(
          data => this.all_mention = data,
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
    this.form.get('plugged')?.setValue('');
    this.form.get('last_num_carte')?.setValue('');
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/mentions/`+uuid, this.options).subscribe(
      data => {
        this.form.get('title')?.setValue(data.title),
        this.form.get('abbreviation')?.setValue(data.abbreviation),
        this.form.get('plugged')?.setValue(data.plugged),
        this.form.get('last_num_carte')?.setValue(data.last_num_carte)},
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
