import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Journey } from '@app/models/journey';
import { QueryParams } from '@app/models/query';
import { ResponseModel } from '@app/models/response';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class JourneyService {
  constructor(
    private http: HttpClient,
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Journey[]>(`${BASE_URL}/journey/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<ResponseModel>(`${BASE_URL}/journey/`,{headers: this.headers});
  }

  getDataByMention(uuid: string){
    let otherParams = new HttpParams().append('uuid_mention', uuid)
    return this.http.get<Journey[]>(`${BASE_URL}/journey/by_uuid_mention/`,{headers: this.headers, params: otherParams});
  }

  deletData(uuid: string):Promise<Journey[]> {
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.delete<Journey[]>(`${BASE_URL}/journey/`, {headers: this.headers, params: otherParams}).toPromise()
  }

  getData(uuid: string){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.get<Journey>(`${BASE_URL}/journey/by_uuid/`, {headers: this.headers, params: otherParams})
  }

  updateData(uuid: string, body: any){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.put<Journey[]>(`${BASE_URL}/journey/`, body, {headers: this.headers, params: otherParams})
  }

  addData(body: any){
    return this.http.post<Journey[]>(`${BASE_URL}/journey/`,body, {headers: this.headers})
  }
}
