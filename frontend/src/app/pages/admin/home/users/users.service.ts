import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '@app/models';
import { CollegeYear } from '@app/models/collegeYear';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';


const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class UsersService {

  constructor(private http: HttpClient) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<User[]>(`${BASE_URL}/users/get_all`, {headers: this.headers, params: params_});
  }

  deletData(uuid: string):Promise<User[]> {
    return this.http.delete<User[]>(`${BASE_URL}/users/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<User>(`${BASE_URL}/users/by_uuid/`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<User>(`${BASE_URL}/users/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    console.log(body)
    return this.http.post<User>(`${BASE_URL}/users/`,body, this.options)
  }
}
