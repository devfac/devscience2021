import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';
import { CollegeYear } from '@app/models/collegeYear';
import { ResponseModel } from '@app/models/response';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class CollegeYearService {

  constructor(private http: HttpClient) { }

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  }
  )


  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<CollegeYear[]>(`${BASE_URL}/college_year/`, {headers: this.headers, params: params_});
  }
  getDataPromise() {
    return this.http.get<ResponseModel>(`${BASE_URL}/college_year/`,this.options);
  }

  deletData(uuid: string):Promise<CollegeYear[]> {
    return this.http.delete<CollegeYear[]>(`${BASE_URL}/college_year/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<CollegeYear>(`${BASE_URL}/college_year/`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<CollegeYear>(`${BASE_URL}/college_year/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<CollegeYear>(`${BASE_URL}/college_year/`,body, this.options)
  }
}
