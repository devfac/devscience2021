import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { StudentInfo } from '@app/models/student';
import { Ue, UeEc } from '@app/models/ue';
import { environment } from '@environments/environment';
import { DownloadService } from '../../download.service';
import { UtilsService } from '../../utils.service';
import { HomeService } from '../home.service';
import { AuthService } from '@app/services/auth/auth.service';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-details-note',
  templateUrl: './details-note.component.html',
  styleUrls: ['./details-note.component.less']
})
export class DetailsNoteComponent implements OnInit {

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  options = {
    headers: this.headers
  }
  infoStudent: StudentInfo = {info:null, Normal: null, Rattrapage: null}
  matier: UeEc[] = []
  allColumns: any[] = []
  form!: FormGroup;
  semester!: string | null;
  isSpinning: boolean = false
  check: boolean = false
  initialise: boolean = false
  disabled: boolean = false
  constructor(
    private http: HttpClient,
    private fb: FormBuilder, 
    public utils: UtilsService,
    private utilsService: UtilsService,
    private service: HomeService,
    public authService: AuthService, 
    ) { 
      this.form = this.fb.group({
        name: [null],
        mention: [null],
        journey: [null],
        semester: [null],
        note: [null],
        isSelected: [null]
      })
    }


  getColumsType(str: string): string{
    return str.substring(0,3)
  }

  getColumsName(str: string): string{
    return str.substring(3)
  }
  getStatus(normal: number, rattrapage: number): string {
    if(Number(normal) <  Number(rattrapage)){
      return 'sup'
    }else if(Number(normal) ===  Number(rattrapage)){
      return 'egal'
    }else if(Number(normal) >  Number(rattrapage)){
      return 'inf'
    }else{
      return ''
    }
  }
  async ngOnInit(){
    this.disabled = this.authService.getPermissionSuperuser()
    this.isSpinning = true 
    if(localStorage.getItem('semester') !== null){
      this.semester = localStorage.getItem('semester')
    }

    this.matier = await this.service.getMatier(localStorage.getItem('collegeYear'), this.semester, localStorage.getItem('journey')).toPromise()

    this.http.get<any>(`${BASE_URL}/notes/view_details?schema=`+localStorage.getItem('collegeYear')+
    `&semester=`+localStorage.getItem('semester')+
    `&uuid_journey=`+localStorage.getItem('journey')+
    `&num_carte=`+localStorage.getItem('numDetails'), this.options).subscribe(
      data => {
        this.infoStudent = data
        this.form.get('name')?.setValue(data.info.last_name+" "+data.info.first_name)
        this.form.get('mention')?.setValue(data.info.journey.mention.title)
        this.form.get('journey')?.setValue(data.info.journey.title)
        this.form.get('semester')?.setValue(data.info.inf_semester+" | " +data.info.sup_semester)
        this.form.get('isSelected')?.setValue(data.info.validation)
        this.check = data.info.validation
        this.isSpinning = false 
        this.initialise = true
    },
      error => {console.error("error as ", error)
    }
    )

  }
  async changeValidation(){
  let validation: any = {}
  if (this.initialise){
    if (this.check){
      for (let index = 1; index<= 10; index++){
        if ("S"+index === this.semester) {
            validation["s"+index] = 'null'; 
            break;
        }
      }
    }else{
      for (let index = 1; index<= 10; index++){
        if ("S"+index === this.semester) {
            validation["s"+index] = localStorage.getItem('collegeYear');
            break;
        }
      }
    }
    this.check = !this.check
     await this.service.createValidation(this.infoStudent.info.num_carte, validation, this.semester).toPromise()
  }
  }
async relever(){
  let year = localStorage.getItem('collegeYear')
  let journey = localStorage.getItem('journey')
  if( year !== null && journey !== null && this.semester){
    let url: string = `${BASE_URL}/scolarites/relever`;
    let params = new HttpParams()
    .append('num_carte', this.infoStudent.info.num_carte)
    .append('college_year', year)
    .append('uuid_journey', journey)
    .append('semester', this.semester)
  let name = "relever "+this.infoStudent.info.num_carte
  this.utilsService.download(url, params, name)
}
  }
/*
  relever(): void{
    const url: string = `${BASE_URL}/scolarites/relever?num_carte=`+this.infoStudent.info.num_carte+
    `&college_year=`+localStorage.getItem('collegeYear')+`&uuid_journey=`+localStorage.getItem('journey')+
    `&semester=`+this.semester
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        a.download = "relever"+this.infoStudent.info.num_carte+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }
*/

  expandSet = new Set<string>();
  onExpandChange(id: string, checked: boolean): void {
    if (checked) {
      this.expandSet.add(id);
    } else {
      this.expandSet.delete(id);
    }
  }
  listOfData = [
    {
      id: 1,
      name: 'John Brown',
      age: 32,
      expand: false,
      address: 'New York No. 1 Lake Park',
      description: 'My name is John Brown, I am 32 years old, living in New York No. 1 Lake Park.'
    },
    {
      id: 2,
      name: 'Jim Green',
      age: 42,
      expand: false,
      address: 'London No. 1 Lake Park',
      description: 'My name is Jim Green, I am 42 years old, living in London No. 1 Lake Park.'
    },
    {
      id: 3,
      name: 'Joe Black',
      age: 32,
      expand: false,
      address: 'Sidney No. 1 Lake Park',
      description: 'My name is Joe Black, I am 32 years old, living in Sidney No. 1 Lake Park.'
    }
  ];

}
