import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { otherQueryParams, QueryParams } from '@app/models/query';
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
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<AncienStudent[]>(`${BASE_URL}/student/new_inscrit`, {headers: this.headers, 
      params: params_});
  }

  getDataObservable_(params_?: HttpParams): Observable<any> {
    return of([]);
  }

  getDataPromise(semester: string,  uuid_journey: string){ 
    let otherParams = new HttpParams().append('semester', semester).append('uuid_journey', uuid_journey)
    return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/get_by_class`,
    {headers: this.headers, params: otherParams})
  }

  getStudentByNumSelect(numSelect: string, collegeYear: string){
    let otherParams = new HttpParams().append('num_select', numSelect).append('college_year', collegeYear)
    return  this.http.get<AncienStudent>(`${BASE_URL}/student/new_selected/`,
    {headers: this.headers, params: otherParams})
  }

  deletData(uuid: string):Promise<Ue[]> {
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.delete<Ue[]>(`${BASE_URL}/matier_ue/`, 
    {headers: this.headers, params: otherParams}).toPromise()
  }

  getData(uuid: string){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.get<Ue>(`${BASE_URL}/matier_ue/by_uuid/`, 
    {headers: this.headers, params: otherParams})
  }

  updateData(numSelect: string, body: any,  collegeYear: string){
    let otherParams = new HttpParams().append('num_select', numSelect).append('college_year', collegeYear)

    return this.http.put<AncienStudent>(`${BASE_URL}/student/new`, body, 
    {headers: this.headers, params: otherParams})
  }

  addData(body: any){
    return this.http.post<Ue[]>(`${BASE_URL}/student/new/`,body, {headers: this.headers})
  }
   
}
