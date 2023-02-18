import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AncienStudent } from '@app/models/student';
import { Ue } from '@app/models/ue';
import { environment } from '@environments/environment';
import { Observable, of } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class ReInscriptionService {
  constructor(
    private http: HttpClient,
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<AncienStudent[]>(`${BASE_URL}/student/ancien/`, {headers: this.headers, 
      params: params_});
  }

  getDataPromise(semester: string,  uuid_journey: string){ 
    let otherParams = new HttpParams().append('semester', semester).append('uuid_journey', uuid_journey)
    return this.http.get<AncienStudent>(`${BASE_URL}/matier_ue/get_by_class/`,{headers: this.headers, params: otherParams})
  }

  getStudentByNumCarte(numCarte: string, collegeYear: string){
    let otherParams = new HttpParams().append('num_carte', numCarte ).append('college_year', collegeYear)
    return  this.http.get<AncienStudent>(`${BASE_URL}/student/num_carte/`, {headers: this.headers, params: otherParams})
  }

  deletData(numCarte: string):Promise<Ue[]> {
    let otherParams = new HttpParams().append('num_carte', numCarte)
    return this.http.delete<Ue[]>(`${BASE_URL}/student/ancien/`, {headers: this.headers, params: otherParams}).toPromise()
  }
/*
  updateData(numCarte: string, body: any){
    let otherParams = new HttpParams().append('num_carte', numCarte)
    return this.http.put<AncienStudent>(`${BASE_URL}/student/new?num_select=`+numCarte, body, {headers: this.headers})
  }
*/
  addData(body: any, collegeYear:string ){
    let otherParams = new HttpParams().append('college_year', collegeYear)
    return this.http.post<AncienStudent>(`${BASE_URL}/student/ancien/`,body, {headers: this.headers, params: otherParams})
  }
   
}
