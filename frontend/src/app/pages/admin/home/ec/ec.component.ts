import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { ColumnItem, Ec, EcColumn } from '@app/models/ec';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Ue } from '@app/models/ue';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-ec',
  templateUrl: './ec.component.html',
  styleUrls: ['./ec.component.less']
})
export class EcComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  user = localStorage.getItem('user')
  collegeYear = localStorage.getItem('year')
  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  allEc: Ec[] = []
  allUe: Ue[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef;
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  uuid= "";
  data = ""
  actualYear: string = ""
  titles: any[] = []
  

  listOfColumns: ColumnItem[] = [
    {
      name:"Title",
      sortOrder: null,
      sortFn: (a: EcColumn, b:EcColumn) => a.title.localeCompare(b.title),
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Journey",
      sortOrder: null,
      sortFn: (a: EcColumn, b:EcColumn) => a.abbreviation_journey.localeCompare(b.abbreviation_journey),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.titles,
      filterFn:(list: string[], item: EcColumn) => list.some(journey => item.abbreviation_journey.indexOf(journey) !== -1)
    },
    {
      name:"Semester",
      sortOrder: null,
      sortFn: (a: EcColumn, b:EcColumn) => a.semester.localeCompare(b.semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: EcColumn) => item.semester.indexOf(semester) !== -1
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
      name:"Ue",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn:null
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

  options = {
    headers: this.headers
  }

  constructor(private http: HttpClient,  private modal: NzModalService, private fb: FormBuilder) { 
    this.form = this.fb.group({
    title: [null, [Validators.required]],
    semester: [null, [Validators.required]],
    valueUe: [null, [Validators.required]],
    journey: [null, [Validators.required]],
    weight: [null, [Validators.required]],
    mention: [null, [Validators.required]],
    isOptional: [null],
    user: [null, ],
    collegeYear: [null],
  });
  this.http.get<Journey[]>(`${BASE_URL}/journey/`, this.options).subscribe(
    data_journey => {
        for(let i=0; i<data_journey.length; i++){
          this.titles.push(
            {
              text: data_journey[i].abbreviation, value: data_journey[i].abbreviation
            }
          )
        }
        localStorage.setItem('filter', JSON.stringify(this.titles))
    },
  )
}

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }

    this.http.get<Mention[]>(`${BASE_URL}/mentions/`, options).subscribe(
      data => {
        this.allMention = data,
        this.form.get('mention')?.setValue(data[0].uuid)
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


    this.http.get<CollegeYear[]>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.allYears = data,
        this.actualYear = data[0].title
        this.form.get('collegeYear')?.setValue(this.actualYear)
        localStorage.setItem('year', data[0].title)
        this.http.get<Ec[]>(`${BASE_URL}/matier_ec/?schema=`+data[0].title, options).subscribe(
          data => this.allEc = data,
          error => console.error("error as ", error)
        );
      },
      error => console.error("error as ", error)
    );
  }
  showConfirm(name?: string, uuid?: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/matier_ec/?schema=`+this.form.get('collegeYear')?.value+`&uuid=`+uuid, this.options).subscribe(
          data => this.allEc = data,
          error => console.error("error as ", error)
        );
      }
    })
  }
  submitForm(): void {
    if (this.form.valid) {
      const data = {
        title: this.form.value.title,
        uuid_journey: this.form.value.journey,
        weight: this.form.value.weight,
        semester: this.form.value.semester,
        value_ue: this.form.value.valueUe,
        teacher: this.form.value.user,
        value: "",
        key_unique: "",
        is_optional: this.form.value.isOptional
      }
      this.isConfirmLoading = true
      console.error(data)
      if (this.isEdit){
        this.http.put<any>(`${BASE_URL}/matier_ec/?schema=`+this.form.get('collegeYear')?.value+`&uuid=`+this.uuid, data, this.options).subscribe(
          data => this.allEc = data,
          error => console.error("error as ", error)
        )
      }else{
        this.http.post<any>(`${BASE_URL}/matier_ec/`,data, this.options).subscribe(
          data => this.allEc = data,
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
    this.form.reset()
    this.form.get('collegeYear')?.setValue(localStorage.getItem('year'))
    this.form.get('isOptional')?.setValue(false)
  }

  showModalEdit(uuid: string): void{
    this.isEdit = true
    this.uuid = uuid
    this.http.get<any>(`${BASE_URL}/matier_ec/by_uuid/?uuid=`+uuid+`&schema=`+this.form.get('collegeYear')?.value, this.options).subscribe(
      data => {
        console.error(data)
        this.form.get('title')?.setValue(data.title),
        this.form.get('weight')?.setValue(data.weight),
        this.form.get('semester')?.setValue(data.semester)
        this.form.get('mention')?.setValue(data.journey.uuid_mention)
        this.form.get('journey')?.setValue(data.uuid_journey)
        this.form.get('valueUe')?.setValue(data.value_ue)
        this.form.get('user')?.setValue(data.users)
        this.form.get('isOptional')?.setValue(data.is_optional)
        this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
          data_journey => {
              console.error("error as ", data_journey)
              this.allJourney = data_journey
              this.form.get('journey')?.setValue(data.uuid_journey)
          },
          error => {
            this.allJourney = []
            console.error("error as ", error)
          }
        )
      },
      error => console.error("error as ", error)
    );
    this.isvisible = true
  }
  getAllUe(): void{
    if (this.form.get('journey')?.value && this.form.get('semester')?.value)
    this.http.get<any>(`${BASE_URL}/matier_ue/get_by_class?semester=`+this.form.get('semester')?.value+'&uuid_journey='+this.form.get('journey')?.value, this.options).subscribe(
      data => {
          this.allUe = data
      },
      error => {
        this.allUe = []
        console.error("error as ", error)
      }
    )
  }
  getAllJourney(): void{
    this.http.get<any>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
      data => {
          console.error("error as ", data)
          this.allJourney = data
          this.form.get('journey')?.setValue('')
      },
      error => {
        this.allJourney = []
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
