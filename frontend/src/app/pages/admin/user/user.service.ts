import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Menu } from '@app/models/menu';
import { environment } from '@environments/environment';
import { Subject } from 'rxjs';

const BASE_URL = environment.authApiURL;
@Injectable({
  providedIn: 'root'
})
export class UserService {

  private headers =  new HttpHeaders({
    'Accept': 'application/json',
    "Authorization": "Bearer "+localStorage.getItem("token")
  })
  
  constructor(
    private http: HttpClient,
    ) { }
  
  setDefaultValueForm(form: FormGroup, defaultValue: any) {
    form.reset(defaultValue);
    for (const key in form.controls) {
      if (form.controls.hasOwnProperty(key)) {
        form.controls[key].markAsPristine();
        form.controls[key].updateValueAndValidity();
      }
    }
  }

  uploadPhoto(form: FormGroup, formData: FormData){
    return this.http.post<any>(`${BASE_URL}/student/upload_photo/?num_carte=`+form.value.numCarte,formData, {headers: this.headers})
  }
  public menu: Menu[] = [
    {
      id: 0,
      title: 'admin.user.dashboard.title',
      route: 'dashboard',
      selected: '/user/dashboard',
      icon: 'area-chart',
    },
    {
      id: 1,
      title: 'admin.home.teaching',
      route: 'dashboard',
      selected: '/user/dashboard',
      icon: 'robot',
      children: [
        {
          id: 1,
          title: 'admin.user.selection.title',
          route: 'selection',
          selected: '/user/selection',
          icon: 'folder-open',
        },
        {
          id: 2,
          title: 'admin.user.inscription.title',
          route: 'inscription',
          selected: '/user/inscription',
          icon: 'usergroup-add',
        },
        {
          id: 3,
          title: 'admin.user.reinscription.title',
          route: 'reinscription',
          selected: '/user/reinscription',
          icon: 'user-switch',
        },
        {
          id: 4,
          title: 'admin.home.note.title',
          route: 'note',
          selected: '/user/note',
          icon: 'file-done',
        },
        {
          id: 5,
          title: 'admin.user.upload.title',
          route: 'upload',
          selected: '/user/upload',
          icon: 'upload',
        },
      ]
    },
     
    {
      id: 6,
      title: 'admin.home.historic.title',
      route: 'historic',
      selected: '/user/historic',
      icon: 'history',
    }
  ]
  public menu$ = new Subject<any>();
  public showSider = true;
  public showSider$ = new Subject<boolean>();

  setShowSider(show: boolean) {
    this.showSider = show;
    this.showSider$.next(show);
  }
}
