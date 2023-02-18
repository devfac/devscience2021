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
import { User } from '@app/models';
import { NoteService } from '../note/note.service';

const BASE_URL = environment.authApiURL;

@Component({
  selector: 'app-details-note',
  templateUrl: './details-note.component.html',
  styleUrls: ['./details-note.component.less']
})
export class DetailsNoteComponent implements OnInit {



  infoStudent: StudentInfo = {info:null, Normal: null, Rattrapage: null}
  matier: UeEc[] = []
  allColumns: any[] = []
  form!: FormGroup;
  semester: string  = "";
  session: string  = "";
  journey: string  = "";
  isSpinning: boolean = true
  check: boolean = false
  initialise: boolean = false
  disabled: boolean = false
  user!: User
  constructor(
    private http: HttpClient,
    private fb: FormBuilder, 
    public utils: UtilsService,
    private utilsService: UtilsService,
    private service: HomeService,
    private noteService: NoteService,
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
    private headers =  new HttpHeaders({
      'Accept': 'application/json',
      "Authorization": "Bearer "+window.sessionStorage.getItem("token")
    }
    )

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
    this.user = await this.noteService.getMe().toPromise()
    this.disabled = !this.user.is_superuser
    this.semester = localStorage.getItem('semester') || ""
    this.session = localStorage.getItem('session') || ""
    this.journey = localStorage.getItem('journey') || ""
    

    this.matier = await this.service.getMatier(localStorage.getItem('collegeYear'), this.semester, localStorage.getItem('journey')).toPromise()

    const data = await this.http.get<any>(`${BASE_URL}/notes/view_details?schema=`+localStorage.getItem('collegeYear')+
    `&semester=`+localStorage.getItem('semester')+
    `&uuid_journey=`+localStorage.getItem('journey')+
    `&num_carte=`+localStorage.getItem('numDetails'), {headers: this.headers}).toPromise()
    if(data){
      this.infoStudent = data
      this.form.get('name')?.setValue(data.info.last_name+" "+data.info.first_name)
      this.form.get('mention')?.setValue(data.info.journey.mention.title)
      this.form.get('journey')?.setValue(data.info.journey.title)
      this.form.get('semester')?.setValue(data.info.inf_semester+" | " +data.info.sup_semester)
      this.form.get('isSelected')?.setValue(data.info.validation)
      this.check = data.info.validation
      this.isSpinning = false 
      this.initialise = true
    }
  }

  async changeValidation(){
  if (this.initialise){
    const validation: any = {num_carte:localStorage.getItem('numDetails') ,validation: this.form.get('isSelected')?.value}
    console.log(validation);
    
    this.check = !this.check
     await this.service.createValidation(this.infoStudent.info.num_carte, validation, this.semester, this.session, this.journey).toPromise()
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
  expandSet = new Set<string>();
  onExpandChange(id: string, checked: boolean): void {
    if (checked) {
      this.expandSet.add(id);
    } else {
      this.expandSet.delete(id);
    }
  }

}
