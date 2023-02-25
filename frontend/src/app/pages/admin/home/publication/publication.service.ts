import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Classroom } from '@app/models/classroom';
import { Publication } from '@app/models/publication';
import { ResponseModel } from '@app/models/response';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class PublicationService {
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
    return this.http.get<Publication[]>(`${BASE_URL}/publication/admin`, {headers: this.headers, params: params_});
  }

  getDataPromisee() {
    return this.http.get<ResponseModel>(`${BASE_URL}/publication/`, {headers: this.headers});
  }

  deletData(uuid: string):Promise<Publication[]> {
    return this.http.delete<Publication[]>(`${BASE_URL}/publication/?uuid=`+uuid, {headers: this.headers}).toPromise()
  }

  getData(uuid: string){
    return this.http.get<Publication>(`${BASE_URL}/publication/?uuid=`+uuid, {headers: this.headers})
  }

  updateData(uuid: string, body: any){
    return this.http.put<Publication[]>(`${BASE_URL}/publication/?uuid=`+uuid, body, {headers: this.headers})
  }

  addData(body: any){
    return this.http.post<Publication[]>(`${BASE_URL}/publication/`,body, {headers: this.headers})
  }

}
