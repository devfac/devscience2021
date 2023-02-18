import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { TotalDash } from '@app/models/dashbord';
import { AuthService } from '@app/services/auth/auth.service';
import { environment } from '@environments/environment';
import { Observable } from 'rxjs';
import { MentionService } from '../home/mention/mention.service';

const BASE_URL = environment.authApiURL;

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  
  constructor(
    private http: HttpClient,
    ) { }
   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+window.sessionStorage.getItem("token")
  })

    
  totaldashboard( collegeYear: string){
    let otherParams = new HttpParams()
      .append('college_year', collegeYear)
    return this.http.get<TotalDash>(`${BASE_URL}/statistic/dashboard/`, {headers: this.headers, params: otherParams});
  }
}
