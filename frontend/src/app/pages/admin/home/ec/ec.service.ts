import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Ec } from '@app/models/ec';
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
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Ec[]>(`${BASE_URL}/matier_ec/`, {headers: this.headers, params: params_});
  }
  getDataPromise(){
    return this.http.get<Ec[]>(`${BASE_URL}/matier_ec/`,this.options);
  }

  deletData(uuid: string):Promise<Ec[]> {
    return this.http.delete<Ec[]>(`${BASE_URL}/matier_ec/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Ec>(`${BASE_URL}/matier_ec/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Ec[]>(`${BASE_URL}/matier_ec/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Ec[]>(`${BASE_URL}/matier_ec/`,body, this.options)
  }
   
}
