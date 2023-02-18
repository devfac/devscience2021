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
    "Authorization": "Bearer "+window.sessionStorage.getItem('token')
  })
  
  constructor(
    private http: HttpClient,
    ) { }
    uploadFile(formData: FormData, table_name: string, uuid_mention: string, uuid_journey: string, college_year: string) :Observable<any>{
    let otherParams = new HttpParams().append('model_name', table_name)
                                      .append('uuid_mention', uuid_mention)
                                      .append('uuid_journey', uuid_journey)
                                      .append('college_year', college_year)
      return this.http.post<any>(`${BASE_URL}/save_data/uploadfile/`,formData, {headers: this.headers, params:otherParams})
    }

    saveData(listData:any, uuid_mention: string, uuid_journey: string, college_year: string) :Observable<any>{
      let otherParams = new HttpParams().append('uuid_mention', uuid_mention)
                                        .append('uuid_journey', uuid_journey)
                                        .append('college_year', college_year)
        return this.http.post<any>(`${BASE_URL}/student/list/`,listData, {headers: this.headers, params:otherParams})
      }

    fakeData() :Observable<any>{
        return of({data:[], count: 0})
      }
}
