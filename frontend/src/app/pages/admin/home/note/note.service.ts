import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CollegeYear } from '@app/models/collegeYear';
import { environment } from '@environments/environment';


const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class NoteService {

   
  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  options = {
    headers: this.headers
  }
  constructor(
    private http: HttpClient) { }

  testNote(semester: string, journey: string, session: string){
    return  this.http.get<boolean>(`${BASE_URL}/notes/test_note?semester=`+semester+`&session=`+session+
                                    `&uuid_journey=`+journey, this.options)
  }

  getAllColumns(semester: string, journey: string, session: string, collegeYear: string){
    return this.http.get<any>(`${BASE_URL}/notes/?semester=`+semester+`&session=`+session+`&college_year=`+collegeYear+
                        `&uuid_journey=`+journey, this.options)
  }

  getAllNote(semester: string, journey: string, session: string, collegeYear: string){
   return  this.http.get<any>(`${BASE_URL}/notes/get_all_notes?semester=`+semester+`&session=`+session+
                          `&uuid_journey=`+journey+
                          `&college_year=`+collegeYear, this.options)
                        }
  
}
