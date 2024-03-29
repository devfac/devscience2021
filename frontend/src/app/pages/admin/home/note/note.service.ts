import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CollegeYear } from '@app/models/collegeYear';
import { Mention } from '@app/models/mention';
import { Permission } from '@app/models/permission';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';
import { MentionService } from '../mention/mention.service';
import { User } from '@app/models/user';


const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class NoteService {


  constructor(
    private http: HttpClient,
    private serviceMention: MentionService,
    private authUser: AuthService,
    ) { }

    private headers =  new HttpHeaders({
      'Accept': 'application/json',
      "Authorization": "Bearer "+window.sessionStorage.getItem("token")
    })


  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<any[]>(`${BASE_URL}/notes/get_all_notes/`, {headers: this.headers, params: params_});
  }

  testNote(semester: string, journey: string, session: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('uuid_journey', journey)
    return  this.http.get<boolean>(`${BASE_URL}/notes/test_note/`, {headers: this.headers, params: otherParams})
  }

  getNoteSuccess(semester: string, journey: string, session: string, collegeYear: string, ){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('uuid_journey', journey)
    return  this.http.get<boolean>(`${BASE_URL}/notes/test_note/`, {headers: this.headers, params: otherParams})
  }

  deleteNote(semester: string, journey: string,numCarte: string, session: string, collegeYear: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('uuid_journey', journey)
      .append('num_carte', numCarte)
      .append('college_year', collegeYear)
    return  this.http.delete<any>(`${BASE_URL}/notes/student/`, {headers: this.headers, params: otherParams})
  }

  deleteTable(semester: string, journey: string, session: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('uuid_journey', journey)
    return  this.http.delete<any>(`${BASE_URL}/notes/`, {headers: this.headers, params: otherParams})
  }

  getAllColumns(semester: string, journey: string, session: string, collegeYear: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('college_year', collegeYear)
      .append('uuid_journey', journey)
    return this.http.get<any>(`${BASE_URL}/notes/`, {headers: this.headers, params: otherParams})
  }

  insertStudent(semester: string, journey: string, session: string, collegeYear: string, mention: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('college_year', collegeYear)
      .append('uuid_journey', journey)
      .append('uuid_mention', mention)
    return this.http.post<any>(`${BASE_URL}/notes/insert_students`,null,{headers: this.headers, params: otherParams})
  }

  insertNote(semester: string, journey: string, session: string, collegeYear: string, body: any){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('session', session)
      .append('college_year', collegeYear)
      .append('uuid_journey', journey)
    return this.http.post<any>(`${BASE_URL}/notes/insert_note/`, body, {headers: this.headers, params: otherParams})
  }

  addInteraction(semester: string, body: any){
    let otherParams = new HttpParams()
      .append('semester', semester)
    return this.http.post<any>(`${BASE_URL}/interaction/`, body, {headers: this.headers, params: otherParams})
  }

  getPermission(email: string = '', type_: any){
    let otherParams = new HttpParams()
      .append('email', email)
      .append('type_', type_)
    return this.http.get<Permission>(`${BASE_URL}/permission/get_by_email_and_type/`, {headers: this.headers, params: otherParams})
  }

  createTableNote(semester: string, journey: string, collegeYear: string){
    let otherParams = new HttpParams()
      .append('semester', semester)
      .append('college_year', collegeYear)
      .append('uuid_journey', journey)
    return  this.http.post<any>(`${BASE_URL}/notes/`,null,{headers: this.headers, params: otherParams})
  }

  async getMentionUser(){
    let allMention: Mention[] = []
    const user = this.authUser.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let mention = await this.serviceMention.getData(user?.uuid_mention[i]).toPromise()
      allMention.push(mention)
    }
    return allMention
  }

  uploadFile(formData: FormData, semester: string, session: string, uuid_journey: string, college_year: string) :Observable<any>{
    let otherParams = new HttpParams().append('semester', semester)
                                      .append('session', session)
                                      .append('uuid_journey', uuid_journey)
                                      .append('college_year', college_year)
      return this.http.post<any>(`${BASE_URL}/save_data/upload_note_file/`,formData, {headers: this.headers, params:otherParams})
    }

    getMe(){
      return this.http.get<User>(`${BASE_URL}/users/me`, {headers: this.headers})
    }
}
