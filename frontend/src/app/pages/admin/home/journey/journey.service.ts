import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Journey } from '@app/models/journey';
import { QueryParams } from '@app/models/query';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class JourneyService {

  constructor(private http: HttpClient) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Journey[]>(`${BASE_URL}/journey/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<Journey[]>(`${BASE_URL}/journey/`,this.options);
  }

  getDataByMention(uuid: string | null){
    return this.http.get<Journey[]>(`${BASE_URL}/journey/by_uuid_mention/?uuid_mention=`+uuid,this.options);
  }

  deletData(uuid: string):Promise<Journey[]> {
    return this.http.delete<Journey[]>(`${BASE_URL}/roles/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Journey>(`${BASE_URL}/journey/by_uuid/`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Journey[]>(`${BASE_URL}/journey/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Journey[]>(`${BASE_URL}/journey/`,body, this.options)
  }
}
