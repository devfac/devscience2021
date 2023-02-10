import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Droit } from '@app/models/droit';
import { User } from '@app/models/user';
import { environment } from '@environments/environment';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class HistoricService {

  constructor(
    private http: HttpClient,
    private coockiService: CookieService
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
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
  
  getMe(){
    return this.http.get<User>(`${BASE_URL}/users/me`, {headers: this.headers})
  }
}
