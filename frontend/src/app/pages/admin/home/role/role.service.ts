import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Role } from '@app/models/role';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class RoleService {

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
    return this.http.get<Role[]>(`${BASE_URL}/roles/`, {headers: this.headers, params: params_});
  }

  getDataPromise(){
    return this.http.get<any>(`${BASE_URL}/roles/`,this.options);
  }

  deletData(uuid: string):Promise<Role[]> {
    return this.http.delete<Role[]>(`${BASE_URL}/roles/?uuid=`+uuid, this.options).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Role>(`${BASE_URL}/roles/by_uuid/?uuid=`+uuid, this.options)
  }

  updateData(uuid: string, body: any){
    return this.http.put<Role[]>(`${BASE_URL}/roles/?uuid=`+uuid, body, this.options)
  }

  addData(body: any){
    return this.http.post<Role[]>(`${BASE_URL}/roles/`,body, this.options)
  }
}
