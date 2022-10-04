import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { ColumnItem, Ue, UeColumn } from '@app/models/ue';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-ue',
  templateUrl: './ue.component.html',
  styleUrls: ['./ue.component.less']
})
export class UeComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  user = localStorage.getItem('user')
  all_years: CollegeYear[] = []
  all_journey: Journey[] = []
  all_mention: Mention[] = []
  all_ue: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  form_years!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  data = ""
  actualYear: string = ""

  options = {
    headers: this.headers
  }

  listOfColumns: ColumnItem[] = [
    {
      name:"Title",
      sortOrder: null,
      sortFn: (a: UeColumn, b:UeColumn) => a.title.localeCompare(b.title),
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Journey",
      sortOrder: null,
      sortFn: (a: UeColumn, b:UeColumn) => a.abbreviation_journey.localeCompare(b.abbreviation_journey),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: [],
      filterFn:(list: string[], item: UeColumn) => list.some(journey => item.abbreviation_journey.indexOf(journey) !== -1)
    },
    {
      name:"Semester",
      sortOrder: null,
      sortFn: (a: UeColumn, b:UeColumn) => a.semester.localeCompare(b.semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: UeColumn) => item.semester.indexOf(semester) !== -1
    },
    {
      name:"Poids",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Action",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn:null
    },
  ]
  constructor(private http: HttpClient,  private modal: NzModalService, private fb: FormBuilder) { }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }

    this.http.get<any>(`${BASE_URL}/mentions/`, options).subscribe(
      data => {
        this.all_mention = data,
        this.form.get('mention')?.setValue(data[0].uuid)
      },
      error => console.error("error as ", error)
    );

    this.http.get<any>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.all_years = data,
        this.actualYear = data[0].title
        this.form.get('collegeYear')?.setValue(this.actualYear)
        this.http.get<any>(`${BASE_URL}/matier_ue/?schema=`+data[0].title, options).subscribe(
          data => this.all_ue = data,
          error => console.error("error as ", error)
        );
      },
      error => console.error("error as ", error)
    );

    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }

    this.form = this.fb.group({
      title: [null, [Validators.required]],
      semester: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      credit: [null, [Validators.required]],
      mention: [null, [Validators.required]],
      collegeYear: [null],
    });
  }
  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/matier_ue/`+uuid+`?schema=`+this.form.get('collegeYear')?.value, this.options).subscribe(
          data => this.all_ue = data,
          error => console.error("error as ", error)
        );
      }
    })
  }
  submitForm(): void {
    if (this.form.valid) {
      const data = {credit: this.form.value.credit}

      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        this.form.get('title')?.disabled
        this.http.put<any>(`${BASE_URL}/matier_ue/`+this.uuid+`?schema=`+this.form.get('collegeYear')?.value, data, this.options).subscribe(
          data => this.all_ue = data,
          error => console.error("error as ", error)
        )
      }else{
        const data = {
          title: this.form.value.title,
          credit: this.form.value.credit,
          uuid_journey: this.form.value.journey,
          semester: this.form.value.semester
        }
        this.http.post<any>(`${BASE_URL}/matier_ue/?schema=`+this.form.get('collegeYear')?.value,data, this.options).subscribe(
          data => this.all_ue = data,
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
    this.form.get('credit')?.setValue('');
    this.form.get('journey')?.setValue('');
    this.form.get('semester')?.setValue('');
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/matier_ue/`+uuid+`?schema=`+this.form.get('collegeYear')?.value, this.options).subscribe(
      data => {
        this.form.get('title')?.setValue(data.title),
        this.form.get('credit')?.setValue(data.credit),
        this.form.get('journey')?.setValue(data.journey.uuid),
        this.form.get('mention')?.setValue(data.journey.uuid_mention),
        this.form.get('semester')?.setValue(data.semester)
        this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
          data_journey => {
              console.error("error as ", data_journey)
              this.all_journey = data_journey
              this.form.get('journey')?.setValue(data.uuid_journey)
          },
          error => {
            this.all_journey = []
            console.error("error as ", error)
          }
        )
      },
      error => console.error("error as ", error)
    );
    this.isvisible = true
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
