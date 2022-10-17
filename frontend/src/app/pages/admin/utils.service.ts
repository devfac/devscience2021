import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  constructor() { }

  convertNumber(value: string, precision: number): number | null {
    if (isNaN(parseFloat(value))) return null;
    return +(Math.round(parseFloat(value) * 10 ** precision) / 10 ** precision).toFixed(precision);
  }

  precision(path: string, precision: number, form: FormGroup) {
    const control = form.get(path);
    control?.patchValue(this.convertNumber(control.value, precision));
  }
}
