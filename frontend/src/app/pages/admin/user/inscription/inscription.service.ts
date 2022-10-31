import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { QueryParams } from '@app/models/query';
import { AncienStudent } from '@app/models/student';
import { Ue } from '@app/models/ue';
import { environment } from '@environments/environment';
import { Observable, of } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class InscriptionService {

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
    return this.http.get<AncienStudent[]>(`${BASE_URL}/student/new_inscrit`, {headers: this.headers, 
      params: params_});
  }

  getDataObservable_(params_?: HttpParams): Observable<any> {
    return of([]);
  }

  getDataPromise(semester: string,  uuid_journey: string){ return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/get_by_class?semester=`+
  semester+
  `&uuid_journey=`+uuid_journey,this.options)
  }

  deletData(uuid: string):Promise<Ue[]> {
    return this.http.delete<Ue[]>(`${BASE_URL}/matier_ue/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Ue>(`${BASE_URL}/matier_ue/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Ue[]>(`${BASE_URL}/matier_ue/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Ue[]>(`${BASE_URL}/matier_ue/`,body, this.options)
  }
   
}
