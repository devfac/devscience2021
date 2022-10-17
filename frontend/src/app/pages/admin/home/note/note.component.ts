import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Ue } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { TranslateService } from '@ngx-translate/core';
import { NzModalRef, NzModalService } from 'ng-zorro-antd/modal';
import { DownloadService } from '../../download.service';


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

  allYears: CollegeYear[] = []
  allJourney: Journey[] = []
  allMention: Mention[] = []
  allColumns: any[] = []
  allStudents: any[] = []
  listOfSemester?: string[] = []
  listOfSession = ["Normal" ,"Rattrapage" ,"Final"]
  listOfFilter = ["Moyenne" ,"Credit"]
  confirmModal?: NzModalRef
  form!: FormGroup;
  formDial!: FormGroup;
  isvisible = false;
  isConfirmLoading = false;
  title = '';
  uuid= "";
  data = ""
  value = 10
  matierUe: Ue[]=[];
  matierEc: Ec[]=[];
  valueUe: string = ""
  isSpinning: boolean = false
  isVisible: boolean = false
  searchValue: string = ""
  result: string  = ""
  message: string = ""
  initialise: boolean = false
  visibleDialog: boolean = false
  isResult: boolean = false
  isRattrape: boolean = false
  listOfDisplayData = [...this.allStudents]

  options = {
    headers: this.headers
  }
  constructor(
    private http: HttpClient, 
    private modal: NzModalService, 
    private fb: FormBuilder, 
    public authService: AuthService, 
    private translate: TranslateService,
    private router: Router,
    private downloads: DownloadService,) { 
    this.form = this.fb.group({
      mention: [null, [Validators.required]],
      journey: [null, [Validators.required]],
      session: [null, [Validators.required]],
      collegeYear: [null],
      matierUe: [null],
      matierEc: [null],
      semester: [null, [Validators.required]],
      meanCredit: [null],
      filter: [null],
      salle: [null, [Validators.required]],
      from: [null, [Validators.required]],
      to: [null, [Validators.required]],
    });
}

  editCache: { [key: string]: { edit: boolean; data: any } } = {};

  startEdit(id: string): void {
    this.editCache[id].edit = true;
  }

  cancelEdit(id: string): void {
    const index = this.listOfDisplayData.findIndex(item => item.num_carte === id);
    this.editCache[id] = {
      data: { ...this.listOfDisplayData[index] },
      edit: false
    };
  }

  saveEdit(id: string): void {
    const index = this.listOfDisplayData.findIndex(item => item.num_carte === id);
    this.createModel(this.listOfDisplayData[index], index)
    this.editCache[id].edit = false;
  }

  getColumsType(str: string): string{
    return str.substring(0,3)
  }

  getColumsName(str: string): string{
    return str.substring(3)
  }



  createModel(note:any, index:number): void{
    this.isSpinning = true
    let ue:any[] = []
    for(let i=0;i<this.allColumns.length;i++){
      console.log(this.allColumns[i].value)
      if(this.getColumsType(this.allColumns[i].value) === 'ue_'){
        let ueName = this.getColumsName(this.allColumns[i].value)
        let ec:any[] = []
        for(let j=i+1;j<this.allColumns.length;j++){
          if(this.getColumsType(this.allColumns[j].value) === 'ec_'){
            let ecName = this.getColumsName(this.allColumns[j].value)
            let modelEc = {"name":ecName, "note":note[this.allColumns[j].value]}
            ec.push(modelEc)
          }else{
            break;
          }
        }
        let modelUe = {"name":ueName, "ec":ec}
        ue.push(modelUe)
      }
    }
    let model = {"num_carte":note["num_carte"], "ue":ue}
    console.log(model)
    this.http.post<any>(`${BASE_URL}/notes/insert_note?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, model ,this.options).subscribe(
          data => {
            this.isSpinning = false,
            //this.listOfDisplayData = [...this.allStudents]
            Object.assign(this.listOfDisplayData[index], data);
          },
          error => console.error("error as ", error)
        );
  }
  updateEditCache(): void {
    this.listOfDisplayData.forEach(item => {
      this.editCache[item.num_carte] = {
        edit: false,
        data: item
      };

      console.log( this.editCache[item.num_carte].data['ec_electro_cinetique'])
    });
  }

  compareNoteSupUe(): void{
    if (this.form.value.matierUe){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ue_"+this.form.value.matierUe] >= 10);
      const name = this.matierUe.find((item:Ue) => item.value === this.form.value.matierUe)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ue_admis')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  compareNoteSupEc(): void{
    if (this.form.value.matierEc){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] >= 10);
      const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ec_admis')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  resetTableUe(): void{
    if (this.form.value.matierUe){
      this.result = this.form.value.matierUe
      this.isResult = true
    }else{
      this.listOfDisplayData = this.allStudents;
      this.isResult = false
    }
  }

  resetTableEc(): void{
    if (this.form.value.matierEc){
      this.result = this.form.value.matierEc
      this.isRattrape = true
    }else{
      this.listOfDisplayData = this.allStudents;
      this.isRattrape = false
    }
  }
  getTitle(data: any[], key: string, value: string): any{
    const name = data.find((item: any) => item[key] === value)
    return name
  }

  rattrapageList(): void{
    if (this.form.value.matierEc && this.form.value.session === 'Normal'){
        const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
        this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] < 10 && item["ue_"+name?.value_ue] < 10 )
        this.message = this.listOfDisplayData.length+" "+
        this.translate.instant('admin.home.note.message_ec_refaire')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  changeFilter(){
    if (this.form.value.filter){
      localStorage.setItem('filter', this.form.value.filter)
    }else{
      localStorage.setItem('filter', '')
    }
  }

  filterSup(): void{
    this.message = ""
    if (this.form.value.filter){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'sup')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['moyenne']  >= Number(value) )
        }else{
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['credit']  >= Number(value) )
        }
    }else{
      this.listOfDisplayData = this.allStudents
    }
  }

  filterInf(): void{
    this.message = ""
    if (localStorage.getItem('filter')){
      let value = this.form.value.meanCredit
      localStorage.setItem('lastBtn', 'inf')
        if (localStorage.getItem('filter') === 'Moyenne' ){
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['moyenne']  < Number(value) )
        }else{
          this.listOfDisplayData = this.allStudents.filter((item: any) => item['credit']  < Number(value) )
        }
    }else{
      this.listOfDisplayData = this.allStudents
    }
  }

  compareNoteInfUe(): void{
    if (this.form.value.matierUe){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ue_"+this.form.value.matierUe] < 10);
      const name = this.matierUe.find((item:Ue) => item.value === this.form.value.matierUe)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ue_echec')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }
  test(event: any){
    console.error(event)
  }

  resultat(): void{
    const url: string = `${BASE_URL}/resultat/get_by_matier_pdf?schema=`
    +this.form.get('collegeYear')?.value+`&uuid_journey=`
    +this.form.get('journey')?.value+`&semester=`
    +this.form.get('semester')?.value+`&session=`
    +this.form.get('session')?.value+`&value_ue=`
    +this.form.get('matierUe')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
        a.download = "resultat"+this.form.value.matierUe+"_"+this.form.get('semester')?.value+"_"+journey.abbreviation+"_"+this.form.value.session+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }

  listExam(): void{
    const url: string = `${BASE_URL}/liste/list_exam/?college_year=`
    +this.form.get('collegeYear')?.value+`&uuid_journey=`
    +this.form.get('journey')?.value+`&semester=`
    +this.form.get('semester')?.value+`&session=`
    +this.form.get('session')?.value+`&uuid_mention=`
    +this.form.get('mention')?.value+'&salle='
    +this.form.get('salle')?.value+'&skip='
    +this.form.get('from')?.value+'&limit='
    +this.form.get('to')?.value
    this.downloads
      .download(url, this.options)
      .subscribe(blob => {
        console.log(blob.stream)
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        const journey = this.getTitle(this.allJourney, "uuid", this.form.get('journey')?.value)
        a.download ="List_examen"+this.form.get('semester')?.value+"_"+journey.abbreviation+"salle"
        +this.form.value.salle+"de"+this.form.value.from+"a"
        +this.form.value.to+"session"+this.form.value.session+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }

  compareNoteInfEc(): void{
    if (this.form.value.matierEc){
      this.listOfDisplayData = this.allStudents.filter((item: any) => item["ec_"+this.form.value.matierEc] < 10);
      const name = this.matierEc.find((item:Ec) => item.value === this.form.value.matierEc)
      this.message = this.listOfDisplayData.length+" "+
      this.translate.instant('admin.home.note.message_ec_echec')+" "+name?.title
    }else{
      this.listOfDisplayData = this.allStudents;
      this.message = ""
    }
  }

  setVisible(): void{
    this.isVisible = !this.isVisible
  }
  search(): void {
    this.listOfDisplayData = this.allStudents.filter((item: any) => item.name.indexOf(this.searchValue) !== -1);
  }

  ngOnInit(): void {
    let options = {
      headers: this.headers
    }
    console.log()


    // get College year
    this.http.get<any>(`${BASE_URL}/college_year/`, options).subscribe(
      data => {
        this.allYears = data
        if(localStorage.getItem('collegeYear')){
          this.form.get('collegeYear')?.setValue(localStorage.getItem('collegeYear'))
        }else{
          this.form.get('collegeYear')?.setValue(data[0].title)
          localStorage.setItem('collegeYear', data[0].title)
        }
      },
      error => console.error("error as ", error)
    );
    let test: boolean = false
    // get mention by permission
    if(this.authService.getPermission()){
        const user = this.authService.userValue
        for(let i=0; i<user?.uuid_mention.length;i++){
          this.http.get<Mention>(`${BASE_URL}/mentions/`+user?.uuid_mention[i], this.options).subscribe(
            data =>{
              this.allMention.push(data)
              const name = this.allMention.find((item:Mention) => item.uuid === localStorage.getItem('mention_note'))
              if(name && !test){
                test = true
                this.form.get('mention')?.setValue(localStorage.getItem('mention_note'))
              }
              
              if(localStorage.getItem('mention_note')){
                this.form.get('mention')?.setValue(localStorage.getItem('mention_note'))
              }else{
                this.form.get('mention')?.setValue(data.uuid)
                localStorage.setItem('mention_note', data.uuid)
              }
              },
              error => console.error("error as ", error)
          );
        }
        this.http.get<Journey[]>(`${BASE_URL}/journey/`+localStorage.getItem('mention_note'), this.options).subscribe(
          data_journey => {
              this.allJourney = data_journey
              if(localStorage.getItem('journey_note')){
                this.form.get('journey')?.setValue(localStorage.getItem('journey_note'))

                const journey = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem('journey_note'))
                this.listOfSemester = journey?.semester
              }else{
                this.form.get('journey')?.setValue(data_journey[0].uuid)
                localStorage.setItem('journey_note', data_journey[0].uuid)
                const journey = this.allJourney.find((item: Journey) => item.uuid === data_journey[0].uuid)
                this.listOfSemester = journey?.semester
              }

              if (localStorage.getItem('semester_note')){
                this.form.get('semester')?.setValue(localStorage.getItem('semester_note'));
              }else{
                localStorage.setItem('semester_note',data_journey[0].semester[0])
                this.form.get('semester')?.setValue(localStorage.getItem('semester_note'));
              }

              if (localStorage.getItem('session')){
                this.form.get('session')?.setValue(localStorage.getItem('session'));
              }else{
                localStorage.setItem('session','Normal')
                this.form.get('session')?.setValue(localStorage.getItem('session'));
              }
              this.initialise = true
              this.getAllColumnsSession()
              this.form.get('filter')?.setValue(localStorage.getItem('filter'))
              
          },
          error => {
            this.allJourney = []
            console.error("error as ", error)
          })
    }else{
      this.form.get('salle')?.clearValidators()
      this.form.get('from')?.clearValidators()
      this.form.get('to')?.clearValidators()
      this.http.get<any>(`${BASE_URL}/mentions/`, options).subscribe(
        data => {
          this.allMention = data
          if(localStorage.getItem('mention_note')){
            this.form.get('mention')?.setValue(localStorage.getItem('mention_note'))
          }else{
            this.form.get('mention')?.setValue(data[0].uuid)
            localStorage.setItem('collegeYear', data[0].uuid)
          }
          this.http.get<Journey[]>(`${BASE_URL}/journey/`+localStorage.getItem('mention_note'), this.options).subscribe(
            data_journey => {
                this.allJourney = data_journey
                if(localStorage.getItem('journey_note')){
                  this.form.get('journey')?.setValue(localStorage.getItem('journey_note'))
  
                  const journey = this.allJourney.find((item: Journey) => item.uuid === localStorage.getItem('journey_note'))
                  this.listOfSemester = journey?.semester
                }else{
                  this.form.get('journey')?.setValue(data_journey[0].uuid)
                  localStorage.setItem('journey_note', data_journey[0].uuid)
                  const journey = this.allJourney.find((item: Journey) => item.uuid === data_journey[0].uuid)
                  this.listOfSemester = journey?.semester
                }
  
                if (localStorage.getItem('semester_note')){
                  this.form.get('semester')?.setValue(localStorage.getItem('semester_note'));
                }else{
                  localStorage.setItem('semester_note',data_journey[0].semester[0])
                  this.form.get('semester')?.setValue(localStorage.getItem('semester_note'));
                }
  
                if (localStorage.getItem('session')){
                  this.form.get('session')?.setValue(localStorage.getItem('session'));
                }else{
                  localStorage.setItem('session','Normal')
                  this.form.get('session')?.setValue(localStorage.getItem('session'));
                }
                this.initialise = true
                this.getAllColumnsSession()
            },
            error => {
              this.allJourney = []
              console.error("error as ", error)
            })
        },
        error => console.error("error as ", error)
      );}

  }

  showConfirmStudent(numCarte: string): void{
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer "+numCarte+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/notes/student?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&num_carte='
        +numCarte+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.listOfDisplayData = [...data]},
          error => console.error("error as ", error)
        );
      }
    })
  }


  deleteTable(): void{

    const journey = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
    this.confirmModal = this.modal.confirm({
      nzTitle: "Voulez-vous supprimer la table note "+this.form.get('semester')?.value+" "+journey?.abbreviation+" "+this.form.get('session')?.value+"?",
      nzOnOk: () => {
        this.http.delete<any>(`${BASE_URL}/notes/?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          error => console.error("error as ", error)
        );
      }
    })
  }

  insertStudent(): void{
    if (this.form.valid) {
        this.http.post<any>(`${BASE_URL}/notes/insert_students/?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_mention='
        +this.form.get('mention')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.listOfDisplayData = [... data]
          },
          error => console.error("error as ", error)
        );
      }
  }

  submitForm(): void {
    if (this.form.valid) {
      this.isConfirmLoading = true
        this.http.post<any>(`${BASE_URL}/notes/?schema=`
        +this.form.get('collegeYear')?.value+'&semester='
        +this.form.get('semester')?.value+'&session='
        +this.form.get('session')?.value+'&uuid_journey='
        +this.form.get('journey')?.value, this.options).subscribe(
          data => {
            this.allColumns = data
            this.listOfDisplayData = [...this.allStudents]
          },
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


  getJourney(): void{
    if(this.form.get('mention')?.value && this.initialise){
      this.form.get('journey')?.setValue('')
      this.http.get<Journey[]>(`${BASE_URL}/journey/`+this.form.get('mention')?.value, this.options).subscribe(
        data =>{ 
          this.allJourney=data
          this.form.get('journey')?.setValue(data[0].uuid)
        },
        error => {console.error("error as ", error)
      }
      );
      localStorage.setItem('mention_note', this.form.value.mention)
    }
  }
  changeJourney(): void{
    if(this.form.value.journey && this.initialise){
      localStorage.setItem('journey_note', this.form.value.journey)

      const journey = this.allJourney.find((item: Journey) => item.uuid === this.form.value.journey)
      this.listOfSemester = journey?.semester
    }
  }
  getAllColumnsSession():void{
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('semester')?.value && this.initialise){
      this.isSpinning = true
      this.http.get<Ec[]>(`${BASE_URL}/matier_ec/get_by_class?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => 
            this.matierEc = data,
        error => console.error("error as ", error)
      )

      this.http.get<any[]>(`${BASE_URL}/matier_ue/get_by_class?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => this.matierUe = data,
        error => console.error("error as ", error)
      )

      this.http.get<any[]>(`${BASE_URL}/notes/?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => {
          this.allColumns = []
          for (let i=0; i<data.length; i++){
            if(this.getColumsType(data[i]) === "ec_"){
              const name = this.matierEc.find((item:Ec) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:name?.title, value: data[i]})
            }else{
              const name = this.matierUe.find((item:Ue) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:"UE:"+name?.title, value: data[i]})
            }
          }
        },
        error => console.error("error as ", error)
      )

      this.http.get<any>(`${BASE_URL}/notes/get_all_notes?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => {
          this.allStudents = data,
          this.listOfDisplayData = [...data]
          this.isSpinning = false
          this.updateEditCache()
      },
        error => {console.error("error as ", error),
        this.isSpinning = false
      }
      )

      localStorage.setItem('session', this.form.value.session)
    }
  }
  refresh(): void{
    console.error(this.form.get('session')?.value)
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.form.get('semester')?.value){
      this.isSpinning = true 
      this.http.get<any[]>(`${BASE_URL}/matier_ec/get_by_class?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => this.matierEc = data,
        error => console.error("error as ", error)
      )

      this.http.get<any[]>(`${BASE_URL}/matier_ue/get_by_class?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data =>
            this.matierUe = data,
        error => console.error("error as ", error)
      )

      this.http.get<any>(`${BASE_URL}/notes/?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => {
          this.allColumns = []
          for (let i=0; i<data.length; i++){
            if(this.getColumsType(data[i]) === "ec_"){
              const name = this.matierEc.find((item:Ec) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:"UE:"+name?.title, value: data[i]})
            }else{
              const name = this.matierUe.find((item:Ue) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:name?.title, value: data[i]})
            }
          }
        },
        error => console.error("error as ", error)
      )

      this.http.get<any>(`${BASE_URL}/notes/get_all_notes?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => {
          this.allStudents = data,
          this.isSpinning = false
          this.listOfDisplayData = [...data]
          this.updateEditCache()
        },
        error => {console.error("error as ", error),
        this.isSpinning = false
      }
      )
    }
  }

  getAllColumnsSemester():void{
    if(this.form.get('journey')?.value && this.form.get('mention')?.value && this.form.get('session')?.value && this.initialise){
    this.isSpinning = true
    this.http.get<any[]>(`${BASE_URL}/matier_ec/get_by_class?schema=`+this.form.get('collegeYear')?.value+
    `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
    `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
      data => 
          this.matierEc = data,
      error => console.error("error as ", error)
    )

    this.http.get<any[]>(`${BASE_URL}/matier_ue/get_by_class?schema=`+this.form.get('collegeYear')?.value+
    `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
    `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
      data =>
          this.matierUe = data,
      error => console.error("error as ", error)
    )
      this.http.get<any>(`${BASE_URL}/notes/?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data =>{
          this.allColumns = []
          for (let i=0; i<data.length; i++){
            if(this.getColumsType(data[i]) === "ec_"){
              const name = this.matierEc.find((item:Ec) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:name?.title, value: data[i]})
            }else{
              const name = this.matierUe.find((item:Ue) => item.value === this.getColumsName(data[i]))
              this.allColumns.push({name:"UE:"+name?.title, value: data[i]})
            }
          }
        },
        error => console.error("error as ", error)
      )

      this.http.get<any>(`${BASE_URL}/notes/get_all_notes?schema=`+this.form.get('collegeYear')?.value+
      `&semester=`+this.form.get('semester')?.value+`&session=`+this.form.get('session')?.value+
      `&uuid_journey=`+this.form.get('journey')?.value, this.options).subscribe(
        data => {
          this.allStudents = data,
          this.isSpinning = false,
          this.listOfDisplayData = [...data]
          this.updateEditCache()
      },
        error => {console.error("error as ", error),
        this.isSpinning = false
      }
      )
      localStorage.setItem('semester_note', this.form.value.semester)
    }
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

  showModal(): void{
    this.visibleDialog = true;
  }

  handleCancel(): void{
    this.visibleDialog = false
  }

  viewNoteDetails(num: string): void{
    localStorage.setItem('numDetails', num)
    localStorage.setItem('collegeYear', this.form.value.collegeYear)
    localStorage.setItem('journey', this.form.value.journey)
    localStorage.setItem('semester', this.form.value.semester)
    this.router.navigate(['/user/note-details'])
}

}
