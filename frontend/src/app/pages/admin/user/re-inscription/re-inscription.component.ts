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
import { DownloadService } from '../../download.service';


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
  allYears: CollegeYear[] = []
  allStudents: AncienStudent[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  listOfSemester?: string[] = []
  semesterTitles: any[] = []
  confirmModal?: NzModalRef
  form!: FormGroup;
  formList!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  listOfData: any[] = []
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
    private downloads: DownloadService,
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
      filter: [null],
    });
    this.formList = this.fb.group({
      semester: [null, [Validators.required]],
      journey: [null, [Validators.required]]
    })
  }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      this.http.get<Mention>(`${BASE_URL}/mentions/`+user?.uuid_mention[i], this.options).subscribe(
        data =>{
          this.allMention.push(data)
          this.form.get('mention')?.setValue(data.uuid)

          if(localStorage.getItem('uuid_mention')){
            this.form.get('mention')?.setValue(localStorage.getItem('uuid_mention'))
          }else{
            this.form.get('mention')?.setValue(data.uuid)
            localStorage.setItem('uuid_mention', data.uuid)
          }
          
          },
          error => console.error("error as ", error)
      );
    }


    for(let i=0; i<11; i++){
      this.semesterTitles.push(
        {
          text: "S"+(i+1), value: "S"+(i+1)
        }
      )
    }
    
    this.http.get<CollegeYear[]>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.allYears = data,
        this.form.get('collegeYear')?.setValue(data[0].title)
        if(this.form.get('mention')?.value){
          this.http.get<AncienStudent[]>(`${BASE_URL}/student/ancien?college_year=`+data[0].title+`&uuid_mention=`+this.form.get('mention')?.value, options).subscribe(
            data => {
              this.allStudents = data
              this.listOfData = [...data]
            },
            error => console.error("error as ", error)
          );
        }
      },
      error => console.error("error as ", error)
    );

    this.http.get<Journey[]>(`${BASE_URL}/journey/`+localStorage.getItem("uuid_mention"), this.options).subscribe(
      data =>{ 
        this.allJourney=data
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
          data => this.allStudents = data,
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
      data => {
        this.allStudents = data
        this.listOfData = [...data]
      },
      error => console.error("error as ", error)
    );
    }
  }

  getStudentByNumCarte(): void{
    const numSelect = this.form.get('numSelect')?.value
    if(numSelect && numSelect.length>0){
    this.http.get<AncienStudent>(`${BASE_URL}/student/new_selected?num_select=`+numSelect, this.options).subscribe(
      data =>{ 
        console.log(data)
        this.form.get('mention')?.setValue(data.uuid_mention)
        this.form.get('firstName')?.setValue(data.first_name)
        this.form.get('lastName')?.setValue(data.last_name)
        this.form.get('address')?.setValue(data.address)
        this.form.get('level')?.setValue(data.level)
        this.form.get('dateBirth')?.setValue(data.date_birth)
        this.form.get('placeBirth')?.setValue(data.place_birth)
        this.form.get('sex')?.setValue(data.sex)
        this.form.get('dateCin')?.setValue(data.date_cin)
        this.form.get('placeCin')?.setValue(data.place_cin)
        this.form.get('numCin')?.setValue(data.num_cin)
        this.form.get('sex')?.setValue(data.sex)
        this.form.get('dateCin')?.setValue(data.date_cin)
        this.form.get('placeCin')?.setValue(data.place_cin)
        this.form.get('baccYear')?.setValue(data.baccalaureate_years)
        this.form.get('nation')?.setValue(data.nation)
  },
  error => console.error("error as ", error)
    )
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

  showModal(): void{
    this.isEdit = false;
    this.isvisible = true;
    this.http.get<Journey[]>(`${BASE_URL}/journey/`+localStorage.getItem("uuid_mention"), this.options).subscribe(
      data =>{ 
        this.allJourney=data
      },
      error => console.error("error as ", error)
    );
  }

  download(): void {
    const url: string = `${BASE_URL}/liste/list_inscrit/?college_year=`
    +this.form.get('collegeYear')?.value+`&uuid_journey=`
    +this.formList.get('journey')?.value+'&semester='+this.formList.get('semester')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        const journey = this.allJourney.find((item: Journey) => item.uuid === this.formList.value.journey)
        this.listOfSemester = journey?.semester
        a.download = 'list_etudiants'+journey?.abbreviation+'_'+this.formList.get('semester')?.value+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
      this.isvisible=false
  }


  changeJourney(): void{
    if(this.formList.value.journey ){
      console.log(this.formList.value.journey)
      localStorage.setItem('journey', this.formList.value.journey)

      const journey = this.allJourney.find((item: Journey) => item.uuid === this.formList.value.journey)
      this.listOfSemester = journey?.semester
    }
  }
  changeFilter(){
    if(this.form.value.filter){
      this.listOfData = this.allStudents.filter((item: any) => item.journey.uuid === this.form.value.filter)
    }else{
      this.listOfData = this.allStudents
    }
  }
}
