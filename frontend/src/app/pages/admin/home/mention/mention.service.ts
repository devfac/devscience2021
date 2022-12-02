import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Mention } from '@app/models/mention';
import { ResponseModel } from '@app/models/response';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class MentionService {

  constructor(
    private http: HttpClient,
    public authService: AuthService
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  
  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Mention[]>(`${BASE_URL}/mentions/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<ResponseModel>(`${BASE_URL}/mentions/`,{headers: this.headers});
  }

  deletData(uuid: string):Promise<Mention[]> {
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.delete<Mention[]>(`${BASE_URL}/mentions/`, {headers: this.headers, params: otherParams}).toPromise()
  }

  getData(uuid: string){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.get<Mention>(`${BASE_URL}/mentions/by_uuid/`, {headers: this.headers, params: otherParams})
  }

  updateData(uuid: string, body: any){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.put<Mention[]>(`${BASE_URL}/mentions/`, body, {headers: this.headers, params: otherParams})
  }

  addData(body: any){
    return this.http.post<Mention[]>(`${BASE_URL}/mentions/`,body, {headers: this.headers})
  }
   
  async getMentionUser(){
    let allMention: Mention[] = []
    const user = this.authService.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
      let otherParams = new HttpParams().append('uuid_mention', user?.uuid_mention[i])
     allMention.push( await this.http.get<Mention>(`${BASE_URL}/mentions/`, {headers: this.headers, params: otherParams}).toPromise())
    }
    return allMention
  }
}
