import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Classroom } from '@app/models/classroom';
import { ResponseModel } from '@app/models/response';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';
const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class ClassroomService {
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
    return this.http.get<Classroom[]>(`${BASE_URL}/classroom/`, {headers: this.headers, params: params_});
  }

  getDataPromisee() {
    return this.http.get<ResponseModel>(`${BASE_URL}/classroom/`, {headers: this.headers});
  }

  deletData(uuid: string):Promise<Classroom[]> {
    return this.http.delete<Classroom[]>(`${BASE_URL}/classroom/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Classroom>(`${BASE_URL}/classroom/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Classroom[]>(`${BASE_URL}/classroom/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Classroom[]>(`${BASE_URL}/classroom/`,body, this.options)
  }
   
}
