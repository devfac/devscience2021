import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Droit } from '@app/models/droit';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class HistoricService {

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
    return this.http.get<Droit[]>(`${BASE_URL}/historic/me`, {headers: this.headers, params: params_});
  }

  deletData(uuid: string):Promise<Droit[]> {
    return this.http.delete<Droit[]>(`${BASE_URL}/historic/?uuid=`+uuid, this.options).toPromise()
  }

}
