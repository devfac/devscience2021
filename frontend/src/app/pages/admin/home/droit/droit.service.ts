import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Droit } from '@app/models/droit';
import { Ue } from '@app/models/ue';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class DroitService {
  constructor(
    private http: HttpClient,
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Droit[]>(`${BASE_URL}/droit/`, {headers: this.headers, params: params_});
  }

  deletData(uuid: string):Promise<Droit[]> {
    return this.http.delete<Droit[]>(`${BASE_URL}/droit/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Droit>(`${BASE_URL}/droit/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Droit[]>(`${BASE_URL}/droit/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Droit[]>(`${BASE_URL}/droit/`,body, this.options)
  }
   
}
