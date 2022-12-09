import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';
import { Observable, of } from 'rxjs';

const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class UploadService {

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  
  constructor(
    private http: HttpClient,
    ) { }
    uploadFile(formData: FormData, table_name: string) :Observable<any>{
    let otherParams = new HttpParams().append('model_name', table_name)
      return this.http.post<any>(`${BASE_URL}/save_data/uploadfile/`,formData, {headers: this.headers, params:otherParams})
    }
    fakeData() :Observable<any>{
        return of({data:[], count: 0})
      }
}
