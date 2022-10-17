import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { StudentInfo } from '@app/models/student';
import { Ue, UeEc } from '@app/models/ue';
import { environment } from '@environments/environment';
import { UtilsService } from '../../utils.service';

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
  semester?: any 
  isSpinning: boolean = false
  constructor(
    private http: HttpClient,
    private fb: FormBuilder, 
    public utils: UtilsService
    ) { 
      this.form = this.fb.group({
        name: [null],
        mention: [null],
        journey: [null],
        semester: [null],
        note: [null]
      })
    }


  getColumsType(str: string): string{
    return str.substring(0,3)
  }

  getColumsName(str: string): string{
    return str.substring(3)
  }
  getStatus(normal: number, rattrapage: number): string {
    console.log(Number(normal), Number(rattrapage))
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
  ngOnInit(): void {
    this.isSpinning = true 
    this.semester = localStorage.getItem('semester')

    this.http.get<UeEc[]>(`${BASE_URL}/matier_ue/get_by_class_with_ec?schema=`+localStorage.getItem('collegeYear')+
      `&semester=`+localStorage.getItem('semester')+
      `&uuid_journey=`+localStorage.getItem('journey'), this.options).subscribe(
        data => 
            {this.matier = data
            console.log(data)
          },

        error => console.error("error as ", error)
      )

    this.http.get<any>(`${BASE_URL}/notes/view_details?schema=`+localStorage.getItem('collegeYear')+
    `&semester=`+localStorage.getItem('semester')+
    `&uuid_journey=`+localStorage.getItem('journey')+
    `&num_carte=`+localStorage.getItem('numDetails'), this.options).subscribe(
      data => {
        this.infoStudent = data
        console.log(data)
        this.form.get('name')?.setValue(data.info.last_name+" "+data.info.first_name)
        this.form.get('mention')?.setValue(data.info.journey.mention.title)
        this.form.get('journey')?.setValue(data.info.journey.title)
        this.form.get('semester')?.setValue(data.info.inf_semester+" | " +data.info.sup_semester)
        this.isSpinning = false 
    },
      error => {console.error("error as ", error)
    }
    )

  }

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
