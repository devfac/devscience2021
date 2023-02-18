import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BaccSerie } from '@app/models/bacc-serie';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class BaccSerieService {

  constructor(private http: HttpClient) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }
  
  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<BaccSerie[]>(`${BASE_URL}/bacc_serie/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<any>(`${BASE_URL}/bacc_serie/`,this.options);
  }

  deletData(uuid: string):Promise<BaccSerie[]> {
    return this.http.delete<BaccSerie[]>(`${BASE_URL}/bacc_serie/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<BaccSerie>(`${BASE_URL}/bacc_serie/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<BaccSerie[]>(`${BASE_URL}/bacc_serie/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<BaccSerie[]>(`${BASE_URL}/bacc_serie/`,body, this.options)
  }
}
