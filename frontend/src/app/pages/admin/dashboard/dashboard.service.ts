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
  
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  constructor(
    private http: HttpClient    ) { }
    
  totaldashboard( collegeYear: string){
    let otherParams = new HttpParams()
      .append('college_year', collegeYear)
    return this.http.get<TotalDash>(`${BASE_URL}/statistic/dashboard/`, {headers: this.headers, params: otherParams});
  }
}
