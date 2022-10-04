import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }
  
  setDefaultValueForm(form: FormGroup, defaultValue: any) {
    form.reset(defaultValue);
    for (const key in form.controls) {
      if (form.controls.hasOwnProperty(key)) {
        form.controls[key].markAsPristine();
        form.controls[key].updateValueAndValidity();
      }
    }
  }
}
