import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Ec } from '@app/models/ec';
import { ResponseModel } from '@app/models/response';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class EcService {

  constructor(
    private http: HttpClient,
    ) { }

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })


  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Ec[]>(`${BASE_URL}/matier_ec/`, {headers: this.headers, params: params_});
  }
  getDataPromise(){
    return this.http.get<ResponseModel>(`${BASE_URL}/matier_ec/`,{headers: this.headers});
  }

  deletData(uuid: string):Promise<Ec[]> {
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.delete<Ec[]>(`${BASE_URL}/matier_ec/`, {headers: this.headers, params: otherParams}).toPromise()
  }

  getData(uuid: string){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.get<Ec>(`${BASE_URL}/matier_ec/by_uuid/`, {headers: this.headers, params: otherParams})
  }

  updateData(uuid: string, body: any){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.put<Ec[]>(`${BASE_URL}/matier_ec/`, body, {headers: this.headers, params: otherParams})
  }

  addData(body: any){
    return this.http.post<Ec[]>(`${BASE_URL}/matier_ec/`,body, {headers: this.headers})
  }

  getEc( semester: string, uuidJourney: string){
    let otherParams = new HttpParams().append('semester', semester).append('uuid_journey', uuidJourney)
    return this.http.get<Ec[]>(`${BASE_URL}/matier_ec/get_by_class`, {headers: this.headers, params: otherParams})
  }

}
