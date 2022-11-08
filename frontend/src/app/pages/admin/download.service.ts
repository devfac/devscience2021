import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DownloadService {
  constructor(private http: HttpClient) {}
  download(url: string, headers:HttpHeaders, params: HttpParams): Observable<Blob> {
    return this.http.get(url, {
      responseType: 'blob', headers: headers, params: params
    })
  }
}
