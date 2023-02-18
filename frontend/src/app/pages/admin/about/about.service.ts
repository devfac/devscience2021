import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class AboutService {

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
  getDataObservable(): Observable<any> {
    return this.http.get<any>(`${BASE_URL}/college_year/`,this.options);
  }
}
