import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { Menu } from '@app/models/menu';
import { AncienStudent } from '@app/models/student';
import { Ue, UeEc } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { Subject } from 'rxjs';
const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class HomeService {

   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }
  constructor(
    private http: HttpClient,
    public authService: AuthService, 
    ) { }

  getCollegeYear(){
  return this.http.get<CollegeYear[]>(`${BASE_URL}/college_year/`, this.options)
  }

  async getMentionUser(){
    let allMention: Mention[] = []
    const user = this.authService.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
     allMention.push( await this.http.get<Mention>(`${BASE_URL}/mentions/`+user?.uuid_mention[i], this.options).toPromise())
    }
    return allMention
  }

  getMentionAdmin(){
    return this.http.get<Mention[]>(`${BASE_URL}/mentions/`, this.options)
  }

  deleteMention(uuid?: string){
    return this.http.delete<Mention[]>(`${BASE_URL}/mentions/`+uuid, this.options)
  }

  createMention(data?:any){
    return this.http.post<Mention[]>(`${BASE_URL}/mentions/`, data, this.options)
  }

  updateMention(uuid?: string, data?:any){
    return this.http.put<Mention[]>(`${BASE_URL}/mentions/?uuid=`+uuid, data, this.options)
  }

  getMentionByUuid(uuid: string | null){
    return  this.http.get<Mention>(`${BASE_URL}/mentions/`+uuid, this.options)
  }

  deleteJourney(uuid?: string){
    return this.http.delete<Journey[]>(`${BASE_URL}/journey/`+uuid, this.options)
  }

  updateJourney(uuid?: string, data?:any){
    return this.http.put<Journey[]>(`${BASE_URL}/journey/?uuid=`+uuid, data, this.options)
  }

  createJourney(data?:any){
    return this.http.post<Journey[]>(`${BASE_URL}/journey/`, data, this.options)
  }


  createValidation(num_carte:string, data:any, semester: string, session: string, uuidJourney: string){
    let otherParams = new HttpParams().append('num_carte', num_carte)
    .append('semester', semester)
    .append('session', session)
    .append('uuid_journey', uuidJourney)
    return this.http.post<any[]>(`${BASE_URL}/validation/`, data, {headers: this.headers, params:otherParams})
  }


  getJourneyByUuid(uuid?: string){
    return  this.http.get<Journey>(`${BASE_URL}/journey/by_uuid/`+uuid, this.options)
  }

  getJourneyAdmin(){
    return this.http.get<Journey[]>(`${BASE_URL}/journey/`, this.options)
  }

  getMatier(collegeYear: string | null, semester: string | null, uuidJourney: string | null){
    return this.http.get<UeEc[]>(`${BASE_URL}/matier_ue/get_by_class_with_ec?schema=`+collegeYear+
        `&semester=`+semester+
        `&uuid_journey=`+uuidJourney, this.options)
  }

  getUe( semester: string, uuidJourney: string){
    return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/get_by_class?semester=`+semester+
                              `&uuid_journey=`+uuidJourney, this.options)
  }

  getEc( semester: string, uuidJourney: string){
    return this.http.get<Ec[]>(`${BASE_URL}/matier_ec/get_by_class?semester=`+semester+
                              `&uuid_journey=`+uuidJourney, this.options)
  }

  getStudentByNumSelect(numSelect?: string){
    return  this.http.get<AncienStudent>(`${BASE_URL}/student/new_selected?num_select=`+numSelect, this.options)
  }
  setlValue(form: FormGroup, key: string, value: string, storage: string){
    if (localStorage.getItem(storage)){
      form.get(key)?.setValue(localStorage.getItem(storage))
  }else{
    form.get(key)?.setValue(value)
  }
  }
  public menu: Menu[] = [
    {
    id: 1,
    title: 'admin.home.account',
    route: '/',
    selected: '/home/historic',
    icon: 'account-book',
    
    children: [
      {
        id: 2,
        title: 'admin.home.users.title',
        route: 'users',
        selected: '/home/users',
        icon: 'user',
      },{
        id: 3,
        title: 'admin.home.role.title',
        route: 'role',
        selected: '/home/role',
        icon: 'question-circle',
      },
      {
        id: 4,
        title: 'admin.home.historic.title',
        route: 'historic',
        selected: '/home/historic',
        icon: 'history',
      },
      {
        id: 5,
        title: 'admin.home.permission',
        route: 'permission',
        selected: '/home/permission',
        icon: 'setting',
      },
    ]
    
  },{
    id: 5,
    title: 'admin.home.service',
    route: '/',
    selected: '/home/permission',
    icon: 'control',
    children:[
      {
        id: 7,
        title: 'admin.home.mention.title',
        route: 'mention',
        selected: '/home/mention',
        icon: 'node-expand',
      },
      {
        id: 8,
        title: 'admin.home.journey.title',
        route: 'journey',
        selected: '/home/journey',
        icon: 'apartment',
      },{
        id: 9,
        title: 'admin.home.college_year.title',
        route: 'college-year',
        selected: '/home/college-year',
        icon: 'control',
      },
      {
        id: 10,
        title: 'admin.home.droit.title',
        route: 'droit',
        selected: '/home/droit',
        icon: 'dollar',
      },
      {
        id: 11,
        title: 'admin.home.classroom.title',
        route: 'classroom',
        selected: '/home/classroom',
        icon: 'home',
      },
      {
        id: 12,
        title: 'admin.home.bacc_serie.title',
        route: 'bacc-serie',
        selected: '/home/bacc-serie',
        icon: 'database',
      },
      {
        id: 13,
        title: 'admin.home.publication.title',
        route: 'publication',
        selected: '/home/publication',
        icon: 'radar-chart',
      },
    ]
  },
  
  {
      id: 14,
      title: 'admin.home.teaching',
      route: '/',
      selected: '/home/mention',
      icon: 'robot',
      children: [
        {
          id: 15,
          title: 'admin.home.ue.title',
          route: 'ue',
          selected: '/home/ue',
          icon: 'folder',
        },
        {
          id: 16,
          title: 'admin.home.ec.title',
          route: 'ec',
          selected: '/home/ec',
          icon: 'file-text',
        },
        {
          id: 17,
          title: 'admin.home.note.title',
          route: 'note',
          selected: '/home/note',
          icon: 'file-done',
        },
      ]
    },
   
    
  
  ]
  public menu$ = new Subject<any>();
  public showSider = true;
  public showSider$ = new Subject<boolean>();

  setShowSider(show: boolean) {
    this.showSider = show;
    this.showSider$.next(show);
  }
}