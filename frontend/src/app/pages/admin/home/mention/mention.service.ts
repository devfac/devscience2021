import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Mention } from '@app/models/mention';
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

  options = {
    headers: this.headers
  }
  
  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Mention[]>(`${BASE_URL}/mentions/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<Mention[]>(`${BASE_URL}/mentions/`,this.options);
  }

  deletData(uuid: string):Promise<Mention[]> {
    return this.http.delete<Mention[]>(`${BASE_URL}/mentions/`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Mention>(`${BASE_URL}/mentions/`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Mention[]>(`${BASE_URL}/mentions/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Mention[]>(`${BASE_URL}/mentions/`,body, this.options)
  }
   
  async getMentionUser(){
    let allMention: Mention[] = []
    const user = this.authService.userValue
    for(let i=0; i<user?.uuid_mention.length;i++){
     allMention.push( await this.http.get<Mention>(`${BASE_URL}/mentions/`+user?.uuid_mention[i], this.options).toPromise())
    }
    return allMention
  }
}
