import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Ue, UeEc } from '@app/models/ue';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class UeService {
  constructor(
    private http: HttpClient,
  ) { }

  private headers = new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer " + window.sessionStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }

  getDataObservable(params_?: HttpParams): Observable<any> {
    return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/`, { headers: this.headers, params: params_ });
  }

  getDataPromise(semester: string, uuid_journey: string) {
    return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/get_by_class?semester=` +
      semester +
      `&uuid_journey=` + uuid_journey, this.options)
  }

  deletData(uuid: string): Promise<Ue[]> {
    return this.http.delete<Ue[]>(`${BASE_URL}/matier_ue/?uuid=` + uuid, this.options).toPromise()
  }

  getData(uuid: string) {
    return this.http.get<Ue>(`${BASE_URL}/matier_ue/by_uuid/?uuid=` + uuid, this.options)
  }

  updateData(uuid: string, body: any) {
    return this.http.put<Ue[]>(`${BASE_URL}/matier_ue/?uuid=` + uuid, body, this.options)
  }

  addData(body: any) {
    return this.http.post<Ue[]>(`${BASE_URL}/matier_ue/`, body, this.options)
  }
  getMatier(collegeYear: string | null, semester: string | null, uuidJourney: string | null) {
    return this.http.get<UeEc[]>(`${BASE_URL}/matier_ue/get_by_class_with_ec?` +
      `&semester=` + semester +
      `&uuid_journey=` + uuidJourney, this.options)
  }

  getUe(semester: string, uuidJourney: string) {
    return this.http.get<Ue[]>(`${BASE_URL}/matier_ue/get_by_class?semester=` + semester +
      `&uuid_journey=` + uuidJourney, this.options)
  }
}
