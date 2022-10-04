import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { User } from '@app/models';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Role } from '@app/models/role';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';


const BASE_URL = environment.authApiURL;


@Component({
  selector: 'app-note',
  templateUrl: './note.component.html',
  styleUrls: ['./note.component.less']
})
export class NoteComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  all_years: CollegeYear[] = []
  all_journey: Journey[] = []
  all_mention: Mention[] = []
  all_columns: Mention[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  listOfSession = ["Normal" ,"Rattrapage" ,"Final"]
  confirmModal?: NzModalRef
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
  constructor(private http: HttpClient, private modal: NzModalService, private fb: FormBuilder) { 
    this.form = this.fb.group({
      email: [null, [Validators.required]],
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      session: [null, [Validators.required]],
      collegeYear: [null],
      semester: [null, [Validators.required]],
    });
}

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }

    this.http.get<any>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.all_years = data,
        this.form.get('collegeYear')?.setValue(data[0].title)
      },
      error => console.error("error as ", error)
    );
    
    this.http.get<any>(`${BASE_URL}/mentions/`, options).subscribe(
      data => {
        this.all_mention = data
        this.form.get('mention')?.setValue(data[0].uuid),
        this.form.get('semester')?.setValue("S1"),
        this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
          data_journey => {
              console.error("error as ", data_journey)
              this.all_journey = data_journey
              this.form.get('journey')?.setValue(data_journey[0].uuid)
          },
          error => {
            this.all_journey = []
            console.error("error as ", error)
          })
      },
      error => console.error("error as ", error)
    );
  }
  showConfirm(name: string, uuid: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/users/?uuid=`+uuid, this.options).subscribe(
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

      this.isConfirmLoading = true
        this.http.post<any>(`${BASE_URL}/notes/?uuid=`+this.uuid, this.options).subscribe(
          data => this.all_columns = data,
          error => console.error("error as ", error)
        )
      
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

  handleCancel(): void{
    this.isvisible = false
  }

  getAllColumnsSession():void{
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('semester')?.value){
      this.http.get<any>(`${BASE_URL}/notes/?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => this.all_columns = data,
        error => console.error("error as ", error)
      )
    }
  }

  getAllColumnsSemester():void{
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value){
      this.http.get<any>(`${BASE_URL}/notes/?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => this.all_columns = data,
        error => console.error("error as ", error)
      )
    }
  }


  getAllJourney(): void{
    this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
      data => {
          console.error("error as ", data)
          this.all_journey = data
          this.form.get('journey')?.setValue('')
      },
      error => {
        this.all_journey = []
        console.error("error as ", error)
      }
    )
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }



}
