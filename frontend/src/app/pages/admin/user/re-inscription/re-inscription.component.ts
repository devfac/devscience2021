import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators, ValidatorFn, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router } from '@angular/router';
import { User } from '@app/models';
import { CollegeYear } from '@app/models/collegeYear';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Role } from '@app/models/role';
import { AncienStudent, StudentColumn, ColumnItem } from '@app/models/student';
import { environment } from '@environments/environment';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import {AuthService} from '../../../../services/auth/auth.service'


const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-re-inscription',
  templateUrl: './re-inscription.component.html',
  styleUrls: ['./re-inscription.component.less']
})
export class ReInscriptionComponent implements OnInit {
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  user = localStorage.getItem('user')
  all_years: CollegeYear[] = []
  all_students: AncienStudent[] = []
  all_journey: Journey[] = []
  all_mention: Mention[] = []
  listOfSemester = ["S1" ,"S2" ,"S3" ,"S4" ,"S5" ,"S6" ,"S7" ,"S8" ,"S9" ,"S10"]
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  isEdit = false;
  title = '';
  data = ""
  uuid= "";

  options = {
    headers: this.headers
  }
  listOfColumns: ColumnItem[] = [

    {
      name:"Num carte",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Nom",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.last_name.localeCompare(b.last_name),
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },

    {
      name:"Prenom",
      sortOrder: null,
      sortFn: null,
      sortDirections: ['ascend', 'descend', null],
      filterMultiple: true,
      listOfFilter: [],
      filterFn: null
    },
    {
      name:"Semester inf",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.inf_semester.localeCompare(b.inf_semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: StudentColumn) => item.inf_semester.indexOf(semester) !== -1
    },
    {
      name:"Semester sup",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.sup_semester.localeCompare(b.sup_semester),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: this.semesterTitles,
      filterFn:(semester: string, item: StudentColumn) => item.sup_semester.indexOf(semester) !== -1
    },
    {
      name:"Parcours",
      sortOrder: null,
      sortFn: (a: StudentColumn, b:StudentColumn) => a.journey.abbreviation.localeCompare(b.journey.abbreviation),
      sortDirections: ['ascend','descend', null],
      filterMultiple: false,
      listOfFilter: [],
      filterFn:(list: string[], item: StudentColumn) => list.some(journey => item.journey.abbreviation.indexOf(journey) !== -1)
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

  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public router: Router, 
    private authUser: AuthService) { 


    this.form = this.fb.group({
      email: [null, [Validators.required]],
      firstName: [null, [Validators.required]],
      lastName: [null, [Validators.required]],
      isAdmin: [false],
      mention: [null],
      collegeYear: [null],
      uuidRole: [null, [Validators.required]],
      uuidMention: [[], [Validators.required]],
    });
  }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      this.http.get<Mention>(`${BASE_URL}/mentions/`+user?.uuid_mention[i], this.options).subscribe(
        data =>{
          this.all_mention.push(data)
          this.form.get('mention')?.setValue(data.uuid)
          
          },
          error => console.error("error as ", error)
      );
    }


    for(let i=0; i<this.listOfSemester.length; i++){
      this.semesterTitles.push(
        {
          text: this.listOfSemester[i], value: this.listOfSemester[i]
        }
      )
    }
    
    this.http.get<CollegeYear[]>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.all_years = data,
        this.form.get('collegeYear')?.setValue(data[0].title)
        if(this.form.get('mention')?.value){
          this.http.get<AncienStudent[]>(`${BASE_URL}/student/ancien?college_year=`+data[0].title+`&uuid_mention=`+this.form.get('mention')?.value, options).subscribe(
            data => this.all_students = data,
            error => console.error("error as ", error)
          );
        }
      },
      error => console.error("error as ", error)
    );
  

  }
  showConfirm(name: string, numCarte: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+name+"?",
      nzOnOk: () => {
        this.http.delete<AncienStudent[]>(`${BASE_URL}/student/ancien?num_carte=`+numCarte+'&college_year='+this.form.value.collegeYear+'&uuid_mention='+
        this.form.value.mention, this.options).subscribe(
          data => this.all_students = data,
          error => console.error("error as ", error)
        );
      }
    })
  }
  
  showModalEdit(numCarte: string): void{
    this.isEdit = true
    localStorage.setItem('numCarte', numCarte)
    localStorage.setItem("uuid_mention", this.form.get("mention")?.value)
    localStorage.setItem("college_years", this.form.get("collegeYear")?.value)
    this.router.navigate(['/user/reinscription_add'])
  }


  handleCancel(): void{
    this.isvisible = false
  }

  getAllStudents(): void{
    if(this.form.get('collegeYear')?.value && this.form.get('mention')?.value){
    this.http.get<any>(`${BASE_URL}/student/ancien?college_year=`+this.form.get('collegeYear')?.value+`&uuid_mention=`+this.form.get('mention')?.value, this.options).subscribe(
      data => this.all_students = data,
      error => console.error("error as ", error)
    );
    }
  }

  addStudent():void{
    localStorage.setItem("uuid_mention", this.form.get("mention")?.value)
    localStorage.setItem("college_years", this.form.get("collegeYear")?.value)
    this.router.navigate(['/user/reinscription_add'])
    localStorage.setItem('numCarte', '')
  }

  handleOk(): void{
    setTimeout(() => {
      this.isvisible = false
      this.isConfirmLoading = false
    }, 3000);
  }



}
