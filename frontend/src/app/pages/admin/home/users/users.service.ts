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
  constructor(
    private http: HttpClient,
    ) { }

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<User[]>(`${BASE_URL}/users/get_all`, {headers: this.headers, params: params_});
  }

  getDataPromise() {
    return this.http.get<any>(`${BASE_URL}/users/get_all`, {headers: this.headers});
  }

  deletData(uuid: string):Promise<User[]> {
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.delete<User[]>(`${BASE_URL}/users/`, {headers: this.headers, params: otherParams}).toPromise()
  }

  getData(uuid: string){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.get<User>(`${BASE_URL}/users/by_uuid/`, {headers: this.headers, params: otherParams})
  }

  updateData(uuid: string, body: any){
    let otherParams = new HttpParams().append('uuid', uuid)
    return this.http.put<User>(`${BASE_URL}/users/`, body, {headers: this.headers, params: otherParams})
  }

  addData(body: any){
    return this.http.post<User>(`${BASE_URL}/users/`,body, {headers: this.headers})
  }
}
