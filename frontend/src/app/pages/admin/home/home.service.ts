import { HttpHeaders, HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { CollegeYear } from '@app/models/collegeYear';
import { Ec } from '@app/models/ec';
import { Journey } from '@app/models/journey';
import { Mention } from '@app/models/mention';
import { AncienStudent } from '@app/models/student';
import { Ue, UeEc } from '@app/models/ue';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class HomeService {

   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
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

  getAllJourney(uuidMention: string | null ){
    return this.http.get<Journey[]>(`${BASE_URL}/journey/by_uuid_mention/`+uuidMention, this.options)
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


  createValidation(data?:any, semester?: string | null){
    console.log('uihf iqsgfq jqygsf yqgsf ', data)
    return this.http.post<any[]>(`${BASE_URL}/validation/?semester=`+semester, data, this.options)
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
}