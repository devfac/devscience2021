import { HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { DownloadService } from './download.service';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor(
    private downloads: DownloadService,
    ) { }

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })

  convertNumber(value: string, precision: number): number | null {
    if (isNaN(parseFloat(value))) return null;
    return +(Math.round(parseFloat(value) * 10 ** precision) / 10 ** precision).toFixed(precision);
  }

  precision(path: string, precision: number, form: FormGroup) {
    const control = form.get(path);
    control?.patchValue(this.convertNumber(control.value, precision));
  }

  download(url: string, params: HttpParams, name: string): void{
    this.downloads
      .download(url, this.headers, params)
      .subscribe(blob => {
        const a = document.createElement('a')
        const objectUrl = URL.createObjectURL(blob)
        a.href = objectUrl
        a.download = name+'.pdf';
        a.click();
        URL.revokeObjectURL(objectUrl);
      })
  }
}
